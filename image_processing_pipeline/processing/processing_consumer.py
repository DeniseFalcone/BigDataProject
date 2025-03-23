import os
import json
import logging
import multiprocessing
from kafka import KafkaConsumer
from pymongo import MongoClient

# Load environment variables
# Kafka variables
KAFKA_URL = os.getenv("KAFKA_URL")
KAFKA_TOPIC = os.getenv("KAFKA_BATCH_TOPIC")
# MongoDB variables
MONGO_URL = os.getenv("MONGO_URL")
MONGO_DB = os.getenv("MONGO_DB")
MONGO_PROCESSED_COLLECTION = os.getenv("MONGO_PROCESSED_COLLECTION")


# TODO Takes a batch of images from Kafka and uses them on YOLOv5, saving the results in MongoDB
class BatchFileConsumer(multiprocessing.Process):

    def __init__(self):
        multiprocessing.Process.__init__(self)
        # Logging configuration
        logging.basicConfig(
            format="%(asctime)s - %(levelname)s - %(message)s",
            level=logging.INFO,
            handlers=[logging.StreamHandler()],
            force=True
        )
        # MongoDB connection
        client = MongoClient(MONGO_URL)
        db = client[MONGO_DB]
        self.collection = db[MONGO_PROCESSED_COLLECTION]
        logging.info(f"Connected to MongoDB: {MONGO_URL}, Database: {MONGO_DB}, Collection: {MONGO_PROCESSED_COLLECTION}")
        # Kafka connection
        self.consumer = KafkaConsumer(
            KAFKA_TOPIC,
            bootstrap_servers=KAFKA_URL,
            value_deserializer=lambda v: json.loads(v.decode("utf-8")),
            auto_offset_reset="earliest",
            group_id="batch_processing_group",
            enable_auto_commit=True
        )
        logging.info(f"Connected to Kafka: {KAFKA_URL}, Topic: {KAFKA_TOPIC}")
        self.stop_event = multiprocessing.Event()

    def stop(self):
        self.stop_event.set()


    # TODO Implement the run method to consume messages from Kafka, apply computer vision processing, and save the results in MongoDB
    def run(self):
        try:
            for message in self.consumer:
                logging.info(f"Received message: {message.value}")
        except Exception as e:
            logging.error(f"Error: {e}")
        finally:
            self.consumer.close()
            logging.info("Consumer closed")