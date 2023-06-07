from captureFrames.basicClient import BasicPikaClient

class MQ(BasicPikaClient):
    def __init__(self, brokerID, username, password, region):
        self.basic_message_sender = super().__init__(
            brokerID,
            username,
            password,
            region
        )

    def declare_queue(self, queue_name):
        print(f"Trying to declare queue({queue_name})...")
        self.channel.queue_declare(queue=queue_name, arguments={'x-message-ttl' : 60000})

    def send_message(self, exchange, routing_key, body):
        channel = self.connection.channel()
        channel.basic_publish(exchange=exchange,
                              routing_key=routing_key,
                              body=body)
        print(f"Sent message. Exchange: {exchange}, Routing Key: {routing_key}, Body: {body}")

    def close(self):
        self.channel.close()
        self.connection.close()

    def publish_message(self, message, queue):
        self.declare_queue(queue)
        self.send_message(exchange='', routing_key=queue, body=message)
        self.close()