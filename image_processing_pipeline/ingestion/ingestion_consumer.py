import os
import json
import logging
import multiprocessing
from kafka import KafkaConsumer
from pymongo import MongoClient

# Load environment variables
# Kafka variables
KAFKA_URL = os.getenv("KAFKA_URL")
KAFKA_TOPIC = os.getenv("KAFKA_METADATA_TOPIC")
# MongoDB variables
MONGO_URL = os.getenv("MONGO_URL")
MONGO_DB = os.getenv("MONGO_DB")
MONGO_METADATA_COLLECTION = os.getenv("MONGO_METADATA_COLLECTION")


class MongoMetadataConsumer(multiprocessing.Process):

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
        self.collection = db[MONGO_METADATA_COLLECTION]
        logging.info(f"Connected to MongoDB: {MONGO_URL}, Database: {MONGO_DB}, Collection: {MONGO_METADATA_COLLECTION}")
        # Kafka connection
        self.consumer = KafkaConsumer(
            KAFKA_TOPIC,
            bootstrap_servers=KAFKA_URL,
            value_deserializer=lambda v: json.loads(v.decode("utf-8")),
            auto_offset_reset="earliest",
            group_id="insert-metadata-mongo-group",
            enable_auto_commit=True
        )
        logging.info(f"Connected to Kafka: {KAFKA_URL}, Topic: {KAFKA_TOPIC}")
        self.stop_event = multiprocessing.Event()

    def stop(self):
        self.stop_event.set()

    def run(self):
        try:
            for message in self.consumer:
                logging.info(f"Received message: {message.value}")
                self.collection.insert_one(message.value)
                logging.info(f"Saved to MongoDB: {message.value}")
        except Exception as e:
            logging.error(f"Error: {e}")
        finally:
            self.consumer.close()
            logging.info("Consumer closed")