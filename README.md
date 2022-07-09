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
Hardware:
* a machine with > 16 GB memory and > 15 GB storage

Python:
* python = 3.8.10
* flask = 2.0.3
* flask-pymongo = 2.3.0
* pymongo = 3.12.0
* fasttext = 0.9.2
* gunicorn = 20.1.0

Linux Packages:
* ngrok
* supervisord

## Notes to self
* DBUSERNAME, DBPASSWORD, and FLASKSESSIONKEY are environment variables that have to be set/exported
* Flask's secret key (what I call FLASKSESSIONKEY) can be anything, but it is needed for session data
* If using Docker:
  * the ngrok command in the Dockerfile is incomplete - it needs the ngrok auth token
  * change the command in gunicorn.conf to `python3 -m gunicorn app:app -w 4 -b 0.0.0.0:5000`
  * the flaskproj folder must contain app.py, templates/, and model_trained_on_rockyou_500_epochs.bin
