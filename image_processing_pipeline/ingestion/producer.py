import threading, logging, time
import multiprocessing
from kafka import KafkaProducer
import os

class Producer(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.stop_event = threading.Event()
        
    def stop(self):
        self.stop_event.set()

    def run(self):
        producer = KafkaProducer(bootstrap_servers=os.getenv("KAFKA_BROKER"))

        while not self.stop_event.is_set():
            print("Sending data........")
            producer.send('my-topic', b"test")
            producer.send('my-topic', b"\xc2Hola, mundo!")
            time.sleep(1)

        producer.close()

        
