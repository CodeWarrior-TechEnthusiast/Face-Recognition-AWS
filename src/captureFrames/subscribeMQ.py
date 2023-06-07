from basicClient import BasicPikaClient
import logging
import datetime as dt
from multiprocessing import Queue, Value

logging.basicConfig(filename='app.log', level=logging.INFO, format='%(asctime)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p')
timestamp_queue = Queue()
received_count = Value('i', 0)
total_latency = Value('d', 0.0)

class MQ(BasicPikaClient):
    def __init__(self, brokerID, username, password, region):
        self.basic_message_receiver = super().__init__(
            brokerID,
            username,
            password,
            region
        )

    def consume_messages(self, queue):
        def callback(channel, method, properties, body):
            print(" [x] Received %r" % body)
            if not timestamp_queue.empty():
                time_diff = dt.datetime.now() - timestamp_queue.get()
                latency = "{}.{}".format(time_diff.seconds, time_diff.microseconds)
                print(" [x] Latency: {} seconds".format(latency))
                received_count.value += 1
                total_latency.value += float(latency)
        self.channel.basic_consume(queue=queue, on_message_callback=callback, auto_ack=True)
        print(' [*] Waiting for Results. To exit press CTRL+C')
        try:
            self.channel.start_consuming()
        except:
            pass

    def close(self):
        self.channel.close()
        self.connection.close()
