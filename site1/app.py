import fasttext, random, os, requests
from flask import Flask, render_template, request, current_app, g, session, url_for, redirect
from werkzeug.local import LocalProxy
from flask_pymongo import PyMongo
from markupsafe import escape

app = Flask(__name__)
app.config['MONGO_URI'] = os.environ['DBURI']
app.secret_key = os.environ['FLASKSESSIONKEY']

def get_db():
    db = getattr(g, "_database", None)
    if db is None:
        db = g._database = PyMongo(current_app).db
    return db

db = LocalProxy(get_db)

@app.route('/')
def index():
    s = session['successmsg'] if 'successmsg' in session else ''
    e = session['errormsg'] if 'errormsg' in session else ''
    session['successmsg'] = ''
    session['errormsg'] = ''
    return render_template('index.html', successmsg=s, errormsg=e)

@app.post('/login')
def login():
    username = escape(request.form['username'])
    password = escape(request.form['password'])
    results_doc = db.results.find_one({'username': username})
    if not results_doc:
        results_doc = {'username': username, 'success': 0, 'failures': 0}
        db.results.insert_one(results_doc)
    if verify_user(username, password):
        db.results.update_one({'username': username}, {'$inc': {'success': 1}})
        session['successmsg'] = 'Success!'
    else:
        db.results.update_one({'username': username}, {'$inc': {'failures': 1}})
        session['errormsg'] = 'Invalid username or password!'
    return redirect(url_for('index'))

@app.get('/create')
def createpage():
    return render_template('create.html')

@app.post('/create')
def createaccount():
    username = escape(request.form['username'])
    password = escape(request.form['password'])
    if add_user(username, password):
        session['successmsg'] = 'Account Created!'
        return redirect(url_for('index'))
    session['errormsg'] = 'Username already exists!'
    return redirect(url_for('login'))

@app.post('/forgot')
def forgotpw():
    username = escape(request.form['username'])
    user_doc = db.users.find_one({'username': username})
    password = user_doc['password']

    if escape(request.form['actual']) == "true":
        return password

    k = int(request.form['k']) if 'k' in request.form else 2
    k = k if k <= 5 else 5
    k = k if k > 0 else 1

    include_actual = escape(request.form['include_actual'])

    honeywords = requests.post(os.environ['GCPURL'], json={'password': password, 'k': k, 'include_actual': include_actual}).text.split(',')
    '''
    honeywords=[]
    if include_actual == 'true':
        honeywords.append(obfuscate_pw(password))
    if k-len(honeywords) > 0:
        model = fasttext.load_model("model_trained_on_rockyou_500_epochs.bin")
        temp = model.get_nearest_neighbors(password,k=(k-len(honeywords)))
        for element in temp:
            honeywords.append(obfuscate_pw(element[1]))
    '''
    return {e: 0 for e in honeywords}

@app.post('/getuser')
def getuser():
    return list(db.users.aggregate([{'$sample': {'size': 1}}]))[0]['username']

'''
def obfuscate_pw(password):
    o = list(password)
    n_stars = len(password)//2
    for i in random.sample(range(len(password)), n_stars):
        o[i] = '*'
    return ''.join(o)
'''

def verify_user(username, password):
    user_doc = db.users.find_one({'username': username})
    if user_doc and password == user_doc['password']:
        return True
    return False

def add_user(username, password):
    if db.users.find_one({'username': username}):
        return False
    return db.users.insert_one({'username': username, 'password': password})
