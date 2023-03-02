#!/usr/bin/env python
import pika
import uuid


class FibonacciRpcClient(object):
    def __init__(self):

        credentials = pika.PlainCredentials(username='guest', password='guest')
        parameters = pika.ConnectionParameters(host='rabbitmq',
                                               port=5672,
                                               virtual_host='/',
                                               credentials=credentials
                                               )
        self.connection = pika.BlockingConnection(parameters=parameters)
        self.channel = self.connection.channel()

        result = self.channel.queue_declare(queue='fibonacci')
        self.callback_queue = result.method.queue
        self.channel.basic_consume(on_message_callback=self.on_response, queue=self.callback_queue)

    def on_response(self, ch, method, props, body):
        if self.corr_id == props.correlation_id:
            self.response = body

    def call(self, n):
        self.response = None
        self.corr_id = str(uuid.uuid4())
        self.channel.basic_publish(exchange='',
                                   routing_key='fibonacci',
                                   properties=pika.BasicProperties(
                                       reply_to=self.callback_queue,
                                       correlation_id=self.corr_id,
                                   ),
                                   body=str(n))
        while self.response is None:
            self.connection.process_data_events()
        return int(self.response)


fibonacci_rpc = FibonacciRpcClient()

n = [10, 100, 56]
for i in n:
    print(f' [x] Requesting fibonacci({i})')
    response = fibonacci_rpc.call(str(i))
    print(f'Got {response}')



