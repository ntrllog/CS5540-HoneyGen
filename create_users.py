import uuid
from flask import Flask, render_template, current_app, g, url_for, redirect
from flask_pymongo import PyMongo
from werkzeug.local import LocalProxy

app = Flask(__name__)
app.config['MONGO_URI'] = os.environ['DBURI']

def get_db():
    db = getattr(g, "_database", None)
    if db is None:
        db = g._database = PyMongo(current_app).db
    return db

db = LocalProxy(get_db)

@app.route('/')
@app.route('/<msg>')
def index(msg=''):
    return render_template('create_users.html', msg=msg)

@app.post('/create')
def create_users():
    if db.users.count() >= 100000:
        return redirect(url_for('index', msg='Too many users exist already!'))

    with open('zynga-com_sorted_preprocessed.txt') as f:
        lines = f.read().splitlines()
        for line in lines:
            username = str(uuid.uuid4())
            loop = True
            while loop:
                if db.users.find_one({'username': username}):
                    username = str(uuid.uuid4())
                else:
                    loop = False
            try:
                db.users.insert_one({'username': username, 'password': line})
            except:
                print(username)
                print(line)
                break

    return redirect(url_for('index', msg='Done!'))

if __name__ == "__main__":
    app.run()