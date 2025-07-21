import logging
import time
import os
import threading
from kafka import KafkaProducer
import json
import utils.file_func as file_func

# Load environment variables

# Kafka variables
KAFKA_URL = os.getenv("KAFKA_URL")
KAFKA_TOPIC = os.getenv("KAFKA_PATH_TOPIC")

# DATA FOLDERS
FOLDER_TO_WATCH = os.getenv("FOLDER_TO_WATCH")
FOLDER_TO_WATCH = os.path.realpath(FOLDER_TO_WATCH)
TO_PROCESS_FOLDER = os.getenv("TO_PROCESS_FOLDER")
TO_PROCESS_FOLDER = os.path.realpath(TO_PROCESS_FOLDER)

# Class to watch for new images and send them to Kafka
class NewImagePathProducer(threading.Thread):

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

    def run(self):
        while True:

            new_files = self.new_file_exists()

            if not new_files:
                logging.info("No new files found.")
                time.sleep(10)
                continue

            #logging.info(f"Current files: {new_files}")

            for file in new_files:
                self.send_file_path(file)

            # wait 10 seconds before checking for new files again
            time.sleep(10) 

    def new_file_exists(self):

        all_files = set(os.listdir(FOLDER_TO_WATCH))
        new_files = all_files - set(os.listdir(TO_PROCESS_FOLDER))

        return new_files

    def send_file_path(self, file):
        
        try:
            src_path = os.path.join(FOLDER_TO_WATCH, file)
            dest_path = os.path.join(TO_PROCESS_FOLDER, file)
            file_func.move_file(src_path=src_path, dest_path=dest_path)
            file_path = os.path.join(TO_PROCESS_FOLDER, file)
            message = {"file_path": file_path} 
            self.producer.send(KAFKA_TOPIC, message)
            #logging.info(f"Sent path to Kafka: {message}")
        except Exception as e:
            logging.warning(f"Error processing {file_path}: {e}")
    
    


    


