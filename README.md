# CS5540-HoneyGen

A Flask web app that implements a proposed idea for using representation learning models for password recovery. Enter a username and it returns the top k-nearest neighbors of the user's password obfuscated with stars (`*`).

Idea was suggested by Dionysiou et al. in their paper: HoneyGen: Generating Honeywords Using Representation Learning. Their [source code](https://bitbucket.org/srecgrp/honeygen-generating-honeywords-using-representation-learning/src/master/) was also used and modified.

## Packages
Python:
* python = 3.8.10
* flask = 2.0.3
* flask-pymongo = 2.3.0
* pymongo = 3.12.0
* pymongo[srv]
* fasttext = 0.9.2 (if not using GCP or if generating models - see Generating Models section)
* requests = 2.28.1

## External Services
Database:
* MongoDB
  * 1 database named test
  * 10 collections named results_w1_k1, results_w1_k2, results_w1_k3, results_w2_k1, results_w2_k2, results_w2_k3, results_w3_k1, results_w3_k2, results_w3_k3, users
    * results_w1_k1 stores the results for using 1 website and k = 1
  * don't forget network access configuration!

Cloud Hosting (if local machine doesn't have enough capacity):
* Google Cloud
  * Cloud Storage
    * one bucket that contains the models (see Generating Models section)
      * make sure bucket and model names are changed when creating the function
  * Cloud Function
    * combined model - 4gb memory, timeout >= 300s
    * quarter model - 16gb memory, timeout >= 300s
    * third model - 16gb memory, timeout >= 300s
    * half model - 32gb memory, timeout >= 300s

## Commands to Set Up and Run On Ubuntu
Install stuff
```
sudo apt -y update && sudo apt -y upgrade
sudo apt -y install python3-pip
sudo pip3 install flask pymongo flask-pymongo fasttext requests
sudo pip3 install pymongo[srv]
```

Get the code
```
git clone https://github.com/ntrllog/CS5540-HoneyGen.git
git clone https://bitbucket.org/srecgrp/honeygen-generating-honeywords-using-representation-learning.git
```
  * clone second repo only if generating models (see Generating Models section)

Set environment variables
```
export DBURI=<insert mongodb connection string here>
export FLASKSESSIONKEY=<insert a random string here>
export GCPURL=<insert url here>
```
  * GCPURL is the url of the cloud function

Test it!
```
cd CS5540-HoneyGen/site1/
flask run
```
  * to run another website simultaneously:
     ```
     cd CS5540-HoneyGen/site2/
     flask run -p 5001
     ```

### Running It in a "Production" Setting
These are independent of each other and not steps to be run in order.
* Install and use gunicorn instead of flask's server
* Install and use ngrok to have it accessible from anywhere via a url
* Install and use supervisord to keep it running after leaving the terminal and to have it restarted if it gets interrupted
  * ```
    cd CS5540-HoneyGen/site1/
    sudo mv gunicorn.conf /etc/supervisor/conf.d/
    sudo mv ngrok.conf /etc/supervisor/conf.d/
    sudo unlink /var/run/supervisor.sock
    sudo -E supervisord
    sudo supervisorctl status
    vim /var/log/ngrok.log
    ```
      * if `sudo unlink /var/run/supervisor.sock` returns an error, that is okay
      * the public url is in ngrok.log

## Generating Models
The FastText models are too large (max 12gb for largest model) to store in this repo. Generate models to run locally or upload to Google Cloud Storage.
```
cd honeygen-generating-honeywords-using-representation-learning/
python3 FastText.py
```

### Reduced RockYou Model
Use only 1/4, 1/3, 1/2, 3/4 of the RockYou list for a smaller model. Better similarity than the combined model (below).
```
mv CS5540-HoneyGen/less.py honeygen-generating-honeywords-using-representation-learning/password_lists_processed/
python3 less.py
cd honeygen-generating-honeywords-using-representation-learning/
python3 FastText.py
```
  * replace code in FastText.py accordingly
  * modify less.py to generate custom preprocessed.txt files

### Combined Model
All the passwords from each website in password_lists_processed_50000_records/ combined into one list. The similarity of passwords generated using this model is not good, but it is the smallest model.
```
cd honeygen-generating-honeywords-using-representation-learning/
cat password_lists_processed_50000_records/* > password_lists_processed_50000_records/combined.txt
python3 FastText.py
```
  * replace code in FastText.py accordingly

## Prepopulating Database With Fake Users
```
cp honeygen-generating-honeywords-using-representation-learning/password_lists_processed_50000_records/zynga-com_sorted_preprocessed.txt CS5540-HoneyGen/
cd CS5540-HoneyGen/
python3 create_users.py
```
  * this is also a Flask web app, so run this on localhost

## Misc Notes
* The application calls a Google Cloud Function to load the model from Google Cloud Storage and get the k-nearest neighbors
* DBURI, FLASKSESSIONKEY, GCPURL are environment variables that have to be set/exported
* Flask's secret key (what I call FLASKSESSIONKEY) can be anything, but it is needed for session data
* If using Docker:
  * the ngrok command in the Dockerfile is incomplete - it needs the ngrok auth token
  * if testing, use `flask run --host=0.0.0.0:5000`
  * if running, change the command in gunicorn.conf to `python3 -m gunicorn app:app -w 4 -t 0 -b 0.0.0.0:5000`
  * the flaskproj folder must be created and contain app.py, templates/, and the appropriate model.bin
  * change the directory in gunicorn.conf and ngrok.conf to /flaskproj
