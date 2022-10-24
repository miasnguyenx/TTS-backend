# syntax=docker/dockerfile:1

FROM python:3.8-slim-buster

WORKDIR /flask_app

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt
RUN s
COPY . .    

CMD ["flask", "run", "--host=0.0.0.0"]