import logging
import time
import os
import threading
from pymongo import MongoClient
from kafka import KafkaProducer
import json

# Load environment variables
# Kafka variables
KAFKA_URL = os.getenv("KAFKA_URL")
KAFKA_TOPIC = os.getenv("KAFKA_BATCH_TOPIC")
# Mongodb variables
MONGO_URL = os.getenv("MONGO_URL")
MONGO_DB = os.getenv("MONGO_DB")
MONGO_COLLECTION = os.getenv("MONGO_METADATA_COLLECTION")
# Output file
DATA_FOLDER = os.getenv("DATA_FOLDER")
OUTPUT_FILE = os.path.join(DATA_FOLDER, f"batch_file_{time.strftime('%Y%m%d%H%M%S')}.txt")
# Size of the batch
BATCH_SIZE = 10


class BatchFileProducer(threading.Thread):

    def __init__(self):
        super().__init__()
        logging.basicConfig(
            format="%(asctime)s - %(levelname)s - %(message)s",
            level=logging.INFO,
            handlers=[logging.StreamHandler()],
            force=True
        )
        # MongoDB connection
        client = MongoClient(MONGO_URL)
        db = client[MONGO_DB]
        self.collection = db[MONGO_COLLECTION]
        logging.info(f"Connected to MongoDB: {client}, Database: {db}, Collection: {self.collection}")
        # Kafka producer
        self.producer = KafkaProducer(
            bootstrap_servers=KAFKA_URL,
            value_serializer=lambda v: json.dumps(v).encode("utf-8")
        )
        logging.info(f"Connected to Kafka: {KAFKA_URL}, Topic: {KAFKA_TOPIC}")
 

    def run(self):
        logging.info("BatchFileProducer started...")
        
        while True:
            count = self.collection.count_documents({})
            if count < BATCH_SIZE:
                logging.info(f"Waiting for more documents... Current count: {count}")
                time.sleep(5)  # Wait 5 seconds before checking again
                continue
            documents = list(self.collection.find().limit(BATCH_SIZE))
            file_paths = [doc["file_path"] for doc in documents if "file_path" in doc]
            self.producer.send(KAFKA_TOPIC, {"batch_file_paths": file_paths})
            logging.info(f"Sent batch file to Kafka: {OUTPUT_FILE}")
            # Optionally delete the processed documents
            self.collection.delete_many({"file_path": {"$in": file_paths}})
            logging.info(f"Deleted {len(file_paths)} processed documents from MongoDB")
            time.sleep(5) 


    


    


