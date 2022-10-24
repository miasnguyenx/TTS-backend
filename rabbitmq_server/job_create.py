import json
from tokenize import Number
from unittest import result
import pika
import sys
import time
import random
import string


def job_create():
    id = random.randint(1234, 5678)
    worktime = int(sys.argv[1])
    msg = {
        "id": id,
        "worktime": worktime
    }
    return msg


connection = pika.BlockingConnection(
    pika.ConnectionParameters(host='localhost'))
channel = connection.channel()

channel.exchange_declare(exchange='video', exchange_type='direct')

channel.queue_declare(queue='prepare', durable=True)

message = job_create()

print("Published, Jobid[%d], duration: %d seconds" %
      (message['id'], message['worktime']))

channel.basic_publish(
    exchange='video',
    routing_key='prepare',
    body=json.dumps(message),
    properties=pika.BasicProperties(
        delivery_mode=pika.spec.PERSISTENT_DELIVERY_MODE
    )
)
