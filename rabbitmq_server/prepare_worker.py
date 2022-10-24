#!/usr/bin/env python
from distutils.command.upload import upload
import json
from unittest import result
import pika
import time
import regex as re

connection = pika.BlockingConnection(
    pika.ConnectionParameters(host='localhost'))
channel = connection.channel()
# declare exchange
channel.exchange_declare(exchange='video', exchange_type='direct')
# prepare channel
prepare_channel = channel.queue_declare(queue='prepare', durable=True)
# upload_channel
upload_channel = channel.queue_declare(queue='upload', durable=True)
# get queue name
extract_channel = channel.queue_declare(queue='extract', durable=True)
# bind queue
channel.queue_bind(exchange='video', queue='prepare')
channel.queue_bind(exchange='video', queue="upload")
channel.queue_bind(exchange='video', queue="extract")

print(' [*] Waiting for logs. To exit press CTRL+C')


def execute_prepare(msg):
    msg = json.loads(msg)
    worktime = msg['worktime']
    print("Executing jobid[%d]..., estimate: %d seconds" %
          (msg['id'], msg['worktime']))
    time.sleep(worktime)
    print('Done jobid[%d]' % msg['id'])


def prepare_callback(ch, method, properties, body):
    execute_prepare(body)
    ch.basic_ack(delivery_tag=method.delivery_tag)


channel.basic_qos(prefetch_count=1)
channel.basic_consume(
    queue='prepare', on_message_callback=prepare_callback
)

channel.start_consuming()
