import logging
import time
import os
import threading
from kafka import KafkaProducer
#from watchdog.observers import Observer
#from watchdog.events import FileSystemEventHandler
import pyinotify
from PIL import Image
import json

# Get environment variables
KAFKA_URL = os.getenv("KAFKA_URL")
KAFKA_TOPIC = os.getenv("KAFKA_TOPIC")
WATCH_FOLDER = os.getenv("WATCH_FOLDER")


producer = KafkaProducer(
            bootstrap_servers=KAFKA_URL,
            value_serializer=lambda v: json.dumps(v).encode("utf-8")
        )


def get_metadata(file_path):
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


def send_metadata(file_path):
    try:
        
        # Get metadata
        metadata = get_metadata(file_path)

        # Send metadata to Kafka
        producer.send(KAFKA_TOPIC, metadata)
        logging.info(f"Sent metadata to Kafka: {metadata}")

    except Exception as e:
        logging.warning(f"Error processing {file_path}: {e}")
    

class EventHandler(pyinotify.ProcessEvent):

    def __init__(self):
        super().__init__()

    def process_IN_CREATE(self, event):
        logging.DEBUG(f"New file created: {event.pathname}")
        send_metadata(event.pathname)


class Producer(threading.Thread):

    def __init__(self):
        super().__init__()
        self.seen_files = set(os.listdir(WATCH_FOLDER))


    def run_pyinotify(self):
        logging.info("Starting producer...")
        wm = pyinotify.WatchManager()
        notifier = pyinotify.Notifier(wm, EventHandler())
        wm.add_watch(WATCH_FOLDER, pyinotify.IN_CREATE)
        logging.info(f"Watching folder: {WATCH_FOLDER}")
        notifier.loop()
        logging.info("Producer started, watching for new files...")

        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            notifier.stop()
        finally:
            notifier.join()

    def run(self):
        while True:
            current_files = set(os.listdir(WATCH_FOLDER))
            logging.info(f"Current files: {current_files}")
            new_files = current_files - self.seen_files  # Detect new files
            for file in new_files:
                send_metadata(os.path.join(WATCH_FOLDER, file))
            self.seen_files = current_files
            time.sleep(5)  # Check every second


    


    


