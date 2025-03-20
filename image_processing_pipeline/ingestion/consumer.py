import threading, logging, time
import multiprocessing
from kafka import KafkaConsumer
import os

class Consumer(multiprocessing.Process):
    def __init__(self):
        multiprocessing.Process.__init__(self)
        self.stop_event = multiprocessing.Event()
        
    def stop(self):
        self.stop_event.set()
        
    def run(self):
        consumer = KafkaConsumer(bootstrap_servers=os.getenv("KAFKA_BROKER"),
                                 auto_offset_reset='earliest',
                                 consumer_timeout_ms=1000)
        consumer.subscribe(['my-topic'])
        print("Consumer is going to wait for messages...")

        while not self.stop_event.is_set():
            for message in consumer:
                print("........Receiving data")
                print ("%s:%d:%d: key=%s value=%s" % (message.topic, message.partition,
                                        message.offset, message.key,
                                        message.value))
                if self.stop_event.is_set():
                    break

        consumer.close()