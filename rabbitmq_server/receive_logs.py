#!/usr/bin/env python
import pika

connection = pika.BlockingConnection(
    pika.ConnectionParameters(host='localhost'))
channel = connection.channel()
# declare exchange
channel.exchange_declare(exchange='logs', exchange_type='fanout')
# declare queue
result = channel.queue_declare(queue='', exclusive=True)
# get queue name
queue_name = result.method.queue
# bind queue
channel.queue_bind(exchange='logs', queue=queue_name)

print(' [*] Waiting for logs. To exit press CTRL+C')


def callback(ch, method, properties, body):
    print(" [x] %r" % body)


channel.basic_consume(
    queue=queue_name, on_message_callback=callback, auto_ack=True)

channel.start_consuming()
