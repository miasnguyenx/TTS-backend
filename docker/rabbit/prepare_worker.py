#!/usr/bin/env python
import json
import pika
import time


class workerHelp:
    def channel_initiate(self):
        credentials = pika.PlainCredentials('user', 'bitnami')
        connection = pika.BlockingConnection(
            pika.ConnectionParameters('172.17.0.2', credentials=credentials))
        # connection = pika.BlockingConnection(
        #     pika.ConnectionParameters(host='172.17.0.2'))
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
        return channel

    def execute_prepare(self, msg):
        msg = json.loads(msg)
        worktime = msg['worktime']
        print("Executing jobid[%d]..., estimate: %f seconds" %
            (msg['id'], msg['worktime']))
        time.sleep(worktime)
        print('Done jobid[%d]' % msg['id'])

    def prepare_callback(self, ch, method, properties, body):
        self.execute_prepare(body)
        ch.basic_ack(delivery_tag=method.delivery_tag)

    def process_job(self):
        print('-------------------')
        
        channel = self.channel_initiate()
        channel.basic_qos(prefetch_count=1)
        channel.basic_consume(
            queue='prepare', on_message_callback=self.prepare_callback
        )
        
        print('-------------------')
        channel.start_consuming()

tmp = workerHelp()
tmp.process_job()
