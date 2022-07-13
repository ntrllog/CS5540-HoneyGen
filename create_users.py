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
    if db.users.count() >= 50000:
        return redirect(url_for('index', msg='Too many users exist already!'))

    with open('zynga-com_sorted_preprocessed.txt') as f:
        i = 1
        lines = f.read().splitlines()
        for line in lines:
            username = f"user{i}"
            i += 1
            db.users.insert_one({'username': username, 'password': line})

    return redirect(url_for('index', msg='Done!'))

if __name__ == "__main__":
    app.run()