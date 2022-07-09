FROM ubuntu:20.04

RUN apt update -y && apt upgrade -y && apt install -y python3 python3-pip vim curl supervisor
RUN pip install flask pymongo pymongo[srv] flask-pymongo gunicorn fasttext

COPY flaskproj /flaskproj

COPY gunicorn.conf /etc/supervisor/conf.d/gunicorn.conf
COPY ngrok.conf /etc/supervisor/conf.d/ngrok.conf

RUN curl -s https://ngrok-agent.s3.amazonaws.com/ngrok.asc | tee /etc/apt/trusted.gpg.d/ngrok.asc >/dev/null && echo "deb https://ngrok-agent.s3.amazonaws.com buster main" | tee /etc/apt/sources.list.d/ngrok.list && apt update && apt install ngrok && ngrok config add-authtoken 