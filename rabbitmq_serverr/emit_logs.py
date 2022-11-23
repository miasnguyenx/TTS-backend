#!/usr/bin/env python
import pika
import sys

connection = pika.BlockingConnection(
    pika.ConnectionParameters(host='localhost'))
channel = connection.channel()

# declare exchange type fanout name logs
channel.exchange_declare(exchange='logs', exchange_type='fanout')

# message content
message = ' '.join(sys.argv[1:]) or "info: Hello World!"

# publish message to exchanger, queue name = empty -->
# send messages to all queue ?
channel.basic_publish(exchange='logs', routing_key='', body=message)

# logging
print(" [x] Sent %r" % message)

# close connection
connection.close()
