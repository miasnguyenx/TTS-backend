import json
from tokenize import Number
from unittest import result
import pika
import sys
import time
import random
import string

class jobCreate:  
    def job_initiate(self):
        id = random.randint(1234, 5678)
        worktime = random.uniform(3, 4)
        msg = {
            "id": id,
            "worktime": worktime
        }
        return msg
    
    def message_queue_initiate(self):
        credentials = pika.PlainCredentials('user', 'bitnami')
        # credentials = pika.PlainCredentials('test', 'test')
        # connection = pika.BlockingConnection(
        #     pika.ConnectionParameters(host='172.17.0.2',credentials=credentials))
        connection = pika.BlockingConnection(
            pika.ConnectionParameters(host='172.20.0.2',credentials=credentials))
        # connection = pika.BlockingConnection(
        #     pika.ConnectionParameters(host='172.17.0.2'))
        channel = connection.channel()

        channel.exchange_declare(exchange='video', exchange_type='direct')

        channel.queue_declare(queue='prepare', durable=True)
  
        return channel
        
    def publish_job(self):
        
        channel = self.message_queue_initiate()
        message = self.job_initiate()
        
        channel.basic_publish(
            exchange='video',
            routing_key='prepare',
            body=json.dumps(message),
            properties=pika.BasicProperties(
                delivery_mode=pika.spec.PERSISTENT_DELIVERY_MODE
            )
        )
        print("Published, Jobid[%d], duration: %f seconds" %
            (message['id'], message['worktime']))

publisher = jobCreate()
publisher.publish_job()