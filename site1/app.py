# import fasttext
import random, os, requests
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
    num_websites = int(request.form['numwebsites'])
    k = int(request.form['k'])
    results_doc = db[f"results_w{num_websites}_k{k}"].find_one({'username': username})
    if not results_doc:
        results_doc = {'username': username, 'success': 0, 'failures': 0}
        db[f"results_w{num_websites}_k{k}"].insert_one(results_doc)
    if verify_user(username, password):
        db[f"results_w{num_websites}_k{k}"].update_one({'username': username}, {'$inc': {'success': 1}})
        session['successmsg'] = 'Success!'
    else:
        db[f"results_w{num_websites}_k{k}"].update_one({'username': username}, {'$inc': {'failures': 1}})
        session['errormsg'] = 'Invalid username or password!'
    return redirect(url_for('index'))

@app.post('/forgot')
def forgotpw():
    username = escape(request.form['username'])
    user_doc = db.users.find_one({'username': username})
    password = user_doc['password']

    k = int(request.form['k']) if 'k' in request.form else 2
    k = k if k <= 3 else 3
    k = k if k > 0 else 1

    # comment out if/else if not using GCP
    if k > 1:
        honeywords = requests.post(os.environ['GCPURL'], json={'password': password, 'k': k}).text.split(',')
    else:
        honeywords = [password]

    ''' uncomment this if not using GCP
    honeywords=[]
    honeywords.append(obfuscate_pw(password))
    if k-len(honeywords) > 0:
        model = fasttext.load_model("model_trained_on_rockyou_500_epochs.bin")
        temp = model.get_nearest_neighbors(password,k=(k-len(honeywords)))
        for element in temp:
            honeywords.append(obfuscate_pw(element[1]))
    random.shuffle(honeywords)
    '''

    return {obfuscate_pw(e): 0 for e in honeywords}

@app.post('/getuser')
def getuser():
    return list(db.users.aggregate([{'$sample': {'size': 1}}]))[0]['username']

@app.route('/results')
def showresults():
    w1_k1_results = list(db.results_w1_k1.aggregate([{"$group": {"_id": None, "s_total": {"$sum": "$success"}, "f_total": {"$sum": "$failures"}}}]))
    w1_k1_s = w1_k1_results[0]['s_total'] if len(w1_k1_results) > 0 else 0
    w1_k1_f = w1_k1_results[0]['f_total'] if len(w1_k1_results) > 0 else 0
    w1_k2_results = list(db.results_w1_k2.aggregate([{"$group": {"_id": None, "s_total": {"$sum": "$success"}, "f_total": {"$sum": "$failures"}}}]))
    w1_k2_s = w1_k2_results[0]['s_total'] if len(w1_k2_results) > 0 else 0
    w1_k2_f = w1_k2_results[0]['f_total'] if len(w1_k2_results) > 0 else 0
    w1_k3_results = list(db.results_w1_k3.aggregate([{"$group": {"_id": None, "s_total": {"$sum": "$success"}, "f_total": {"$sum": "$failures"}}}]))
    w1_k3_s = w1_k3_results[0]['s_total'] if len(w1_k3_results) > 0 else 0
    w1_k3_f = w1_k3_results[0]['f_total'] if len(w1_k3_results) > 0 else 0
    w2_k1_results = list(db.results_w2_k1.aggregate([{"$group": {"_id": None, "s_total": {"$sum": "$success"}, "f_total": {"$sum": "$failures"}}}]))
    w2_k1_s = w2_k1_results[0]['s_total'] if len(w2_k1_results) > 0 else 0
    w2_k1_f = w2_k1_results[0]['f_total'] if len(w2_k1_results) > 0 else 0
    w2_k2_results = list(db.results_w2_k2.aggregate([{"$group": {"_id": None, "s_total": {"$sum": "$success"}, "f_total": {"$sum": "$failures"}}}]))
    w2_k2_s = w2_k2_results[0]['s_total'] if len(w2_k2_results) > 0 else 0
    w2_k2_f = w2_k2_results[0]['f_total'] if len(w2_k2_results) > 0 else 0
    w2_k3_results = list(db.results_w2_k3.aggregate([{"$group": {"_id": None, "s_total": {"$sum": "$success"}, "f_total": {"$sum": "$failures"}}}]))
    w2_k3_s = w2_k3_results[0]['s_total'] if len(w2_k3_results) > 0 else 0
    w2_k3_f = w2_k3_results[0]['f_total'] if len(w2_k3_results) > 0 else 0
    w3_k1_results = list(db.results_w3_k1.aggregate([{"$group": {"_id": None, "s_total": {"$sum": "$success"}, "f_total": {"$sum": "$failures"}}}]))
    w3_k1_s = w3_k1_results[0]['s_total'] if len(w3_k1_results) > 0 else 0
    w3_k1_f = w3_k1_results[0]['f_total'] if len(w3_k1_results) > 0 else 0
    w3_k2_results = list(db.results_w3_k2.aggregate([{"$group": {"_id": None, "s_total": {"$sum": "$success"}, "f_total": {"$sum": "$failures"}}}]))
    w3_k2_s = w3_k2_results[0]['s_total'] if len(w3_k2_results) > 0 else 0
    w3_k2_f = w3_k2_results[0]['f_total'] if len(w3_k2_results) > 0 else 0
    w3_k3_results = list(db.results_w3_k3.aggregate([{"$group": {"_id": None, "s_total": {"$sum": "$success"}, "f_total": {"$sum": "$failures"}}}]))
    w3_k3_s = w3_k3_results[0]['s_total'] if len(w3_k3_results) > 0 else 0
    w3_k3_f = w3_k3_results[0]['f_total'] if len(w3_k3_results) > 0 else 0

    return render_template('show_results.html', data=[[w1_k1_s, w1_k2_s, w1_k3_s, w2_k1_s, w2_k2_s, w2_k3_s, w3_k1_s, w3_k2_s, w3_k3_s],[w1_k1_f, w1_k2_f, w1_k3_f, w2_k1_f, w2_k2_f, w2_k3_f, w3_k1_f, w3_k2_f, w3_k3_f]])

def obfuscate_pw(password):
    o = list(password)
    n_stars = len(password)//2
    for i in random.sample(range(len(password)), n_stars):
        o[i] = '*'
    return ''.join(o)

def verify_user(username, password):
    user_doc = db.users.find_one({'username': username})
    if user_doc and password == user_doc['password']:
        return True
    return False
