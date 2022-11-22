# syntax=docker/dockerfile:1

FROM python:3.8-slim-buster

WORKDIR /flask_app

COPY requirements.txt /flask_app
RUN pip3 install -r requirements.txt --no-cache-dir

COPY ./../../ /flask_app/

CMD ["flask", "run", "--host", "0.0.0.0"]