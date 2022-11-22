# syntax=docker/dockerfile:1

FROM python:3.8-slim-buster

WORKDIR /rabbit

COPY requirements.txt /rabbit
RUN pip3 install -r requirements.txt --no-cache-dir

COPY . /rabbit

CMD ["python3", "prepare_worker.py"]