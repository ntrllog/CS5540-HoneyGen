# CS5540-HoneyGen

A Flask web app that implements a proposed idea for using representation learning models for password recovery. Enter a username and it returns the top k-nearest neighbors of the user's password obfuscated with stars (`*`).

```
@inproceedings{dionysiou2021honeygen,
  title={HoneyGen: Generating Honeywords Using Representation Learning},
  author={Dionysiou, Antreas and Vassiliades, Vassilis and Athanasopoulos, Elias},
  booktitle={Proceedings of the 2021 ACM Asia Conference on Computer and Communications Security},
  pages={265--279},
  year={2021}
}
```

Their [source code](https://bitbucket.org/srecgrp/honeygen-generating-honeywords-using-representation-learning/src/master/) was also used and modified.

## Prereqs
Python:
* python = 3.8.10
* flask = 2.0.3
* flask-pymongo = 2.3.0
* pymongo = 3.12.0
* pymongo[srv]
* fasttext = 0.9.2
* gunicorn = 20.1.0
* requests = 2.28.1

Linux Packages:
* ngrok

## Commands to Set Up and Run On Ubuntu Machine
Install stuff
```
sudo apt -y update && sudo apt -y upgrade
sudo apt -y install python3-pip supervisor
sudo pip3 install flask pymongo pymongo[srv] flask-pymongo fasttext gunicorn
curl -s https://ngrok-agent.s3.amazonaws.com/ngrok.asc | sudo tee /etc/apt/trusted.gpg.d/ngrok.asc >/dev/null && echo "deb https://ngrok-agent.s3.amazonaws.com buster main" | sudo tee /etc/apt/sources.list.d/ngrok.list && sudo apt -y update && sudo apt install -y ngrok
```

Get the code
```
git clone https://github.com/ntrllog/CS5540-HoneyGen.git
git clone https://bitbucket.org/srecgrp/honeygen-generating-honeywords-using-representation-learning.git
```

Generate model
```
cd honeygen-generating-honeywords-using-representation-learning/
python3 FastText.py
mv model_trained_on_rockyou_500_epochs.bin ../CS5540-HoneyGen/site1
```
* to generate the combined model:
  ```
  cd honeygen-generating-honeywords-using-representation-learning/
  cat password_lists_processed_50000_records/* > password_lists_processed_50000_records/combined.txt
  python3 FastText.py
  mv model_trained_on_combined_500_epochs.bin ../CS5540-HoneyGen/site1
  ```
  * replace code in FastText.py accordingly

Set credentials
```
export DBUSERNAME=<insert mongodb username here>
export DBPASSWORD=<insert mongodb password here>
export FLASKSESSIONKEY=<insert a random string here>
export GCPURL=<insert url here>
ngrok config add-authtoken <insert ngrok auth token here>
```

Test it!
```
cd ../CS5540-HoneyGen/site1
flask run
```

Run it!
```
cd ../CS5540-HoneyGen/site1
sudo mv gunicorn.conf /etc/supervisor/conf.d/gunicorn.conf
sudo mv ngrok.conf /etc/supervisor/conf.d/ngrok.conf
sudo unlink /var/run/supervisor.sock
sudo -E supervisord
sudo supervisorctl status
vim /var/log/ngrok.log
```
* if `sudo unlink /var/run/supervisor.sock` returns an error, that is okay

## Notes to self
* The application calls a Google Cloud Function to load the model from Google Cloud Storage and get the k-nearest neighbors
* DBUSERNAME, DBPASSWORD, FLASKSESSIONKEY, GCPURL are environment variables that have to be set/exported
* Flask's secret key (what I call FLASKSESSIONKEY) can be anything, but it is needed for session data
* If using Docker:
  * the ngrok command in the Dockerfile is incomplete - it needs the ngrok auth token
  * if testing, use `flask run --host=0.0.0.0:5000`
  * if running, change the command in gunicorn.conf to `python3 -m gunicorn app:app -w 4 -t 0 -b 0.0.0.0:5000`
  * the flaskproj folder must be created and contain app.py, templates/, and the appropriate model.bin
  * change the directory in gunicorn.conf and ngrok.conf to /flaskproj
