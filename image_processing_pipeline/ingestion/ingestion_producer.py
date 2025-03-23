import logging
import time
import os
import threading
from kafka import KafkaProducer
from PIL import Image
import json

# Load environment variables
# Kafka variables
KAFKA_URL = os.getenv("KAFKA_URL")
KAFKA_TOPIC = os.getenv("KAFKA_METADATA_TOPIC")
# Folder to watch for new files
WATCH_FOLDER = os.getenv("WATCH_FOLDER")

class ImageMetadataProducer(threading.Thread):

    def __init__(self):
        super().__init__()
        logging.basicConfig(
            format="%(asctime)s - %(levelname)s - %(message)s",
            level=logging.INFO,
            handlers=[logging.StreamHandler()],
            force=True
        )
        self.producer = KafkaProducer(
            bootstrap_servers=KAFKA_URL,
            value_serializer=lambda v: json.dumps(v).encode("utf-8")
        )
        logging.info(f"Connected to Kafka: {KAFKA_URL}, Topic: {KAFKA_TOPIC}")
        self.seen_files = set(os.listdir(WATCH_FOLDER))

    def run(self):
        while True:
            current_files = set(os.listdir(WATCH_FOLDER))
            logging.info(f"Current files: {current_files}")
            # Check for new files
            new_files = current_files - self.seen_files 
            for file in new_files:
                self.send_metadata(os.path.join(WATCH_FOLDER, file))
            self.seen_files = current_files
            # wait 5 seconds before checking for new files again
            time.sleep(5) 

    def get_metadata(self, file_path):
        with Image.open(file_path) as img:
                width, height = img.size
                img_format = img.format
        file_size = os.path.getsize(file_path)
        metadata = {
            "file_name": os.path.basename(file_path),
            "file_path": file_path,
            "file_size": file_size,
            "width": width,
            "height": height,
            "format": img_format,
            "timestamp": time.time()
        }
        return metadata

    def send_metadata(self, file_path):
        try:
            metadata = self.get_metadata(file_path)
            self.producer.send(KAFKA_TOPIC, metadata)
            logging.info(f"Sent metadata to Kafka: {metadata}")
        except Exception as e:
            logging.warning(f"Error processing {file_path}: {e}")
    
    


    


