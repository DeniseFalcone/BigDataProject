import os
import json
import logging
import multiprocessing
from kafka import KafkaConsumer
from pymongo import MongoClient

# Load environment variables
KAFKA_URL = os.getenv("KAFKA_URL")
KAFKA_TOPIC = os.getenv("KAFKA_TOPIC")
MONGO_URI = os.getenv("MONGO_URI")
MONGO_DB = os.getenv("MONGO_DB")
MONGO_COLLECTION = os.getenv("MONGO_METADATA_COLLECTION")

# Connect to MongoDB
client = MongoClient(MONGO_URI)
db = client[MONGO_DB]
collection = db[MONGO_COLLECTION]

print(f"🛠 Connecting to Kafka: {KAFKA_URL}")

class Consumer(multiprocessing.Process):

    def __init__(self):
        multiprocessing.Process.__init__(self)
        self.stop_event = multiprocessing.Event()

    def stop(self):
        self.stop_event.set()

    def run33333(self):
        consume_messages()

    def run(self):
        consumer = KafkaConsumer(
            KAFKA_TOPIC,
            bootstrap_servers=KAFKA_URL,
            value_deserializer=lambda v: json.loads(v.decode("utf-8")),
            auto_offset_reset="earliest",
            group_id="insert-metadata-mongo-group",
            enable_auto_commit=True
        )
        for message in consumer:
            logging.info(f"Received message: {message.value}")
            dict = {"message": message.value}
            collection.insert_one(dict)
            logging.info(f"Saved to MongoDB: {message.value}")
        


def consume_messages():

    # Set up Kafka Consumer
    consumer = KafkaConsumer(
        KAFKA_TOPIC,
        bootstrap_servers=KAFKA_URL,
        value_deserializer=lambda v: json.loads(v.decode("utf-8")),
        auto_offset_reset="earliest",
        group_id="insert-metadata-mongo-group",
        enable_auto_commit=True
    )

    
    print("✅ Successfully connected to Kafka broker!")


    logging.info(f"Connected to Kafka: {KAFKA_URL}, Topic: {KAFKA_TOPIC}")
    logging.info(f"Connected to MongoDB: {MONGO_URI}, Database: {MONGO_DB}, Collection: {MONGO_COLLECTION}")

    try:
        for message in consumer:
            metadata = message.value
            logging.info(f"Received message: {metadata}")

            # Save to MongoDB
            collection.insert_one(metadata)
            logging.info(f"Saved to MongoDB: {metadata}")

    except Exception as e:
        logging.error(f"Error: {e}")
    finally:
        consumer.close()

