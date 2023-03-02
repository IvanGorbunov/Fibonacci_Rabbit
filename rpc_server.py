#!/usr/bin/env python
import pika

from fibonacci import fibonacci

credentials = pika.PlainCredentials(username='guest', password='guest')
parameters = pika.ConnectionParameters(host='rabbitmq',
                                       port=5672,
                                       virtual_host='/',
                                       credentials=credentials
                                       )
connection = pika.BlockingConnection(parameters=parameters)

channel = connection.channel()

channel.queue_declare(queue='fibonacci')


def on_request(ch, method, props, body):
    if not props.reply_to:
        return

    n = int(body)
    print(f'fibonacci({n})')
    response = fibonacci(n)
    ch.basic_publish(exchange='',
                     routing_key=props.reply_to,
                     properties=pika.BasicProperties(correlation_id=props.correlation_id),
                     body=str(response)
                     )
    ch.basic_ack(delivery_tag=method.delivery_tag)


channel.basic_qos(prefetch_count=1)
channel.basic_consume(queue='fibonacci', on_message_callback=on_request)

print(' [x] Awaiting RPC requests')
channel.start_consuming()
