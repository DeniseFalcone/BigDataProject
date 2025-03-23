import shutil
import os
import time
import logging
import threading

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

WATCH_FOLDER = os.getenv("WATCH_FOLDER")
DATASET_FOLDER = os.getenv("DATA_FOLDER")


class RealTimeDataSimulator(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.dataset_folder = DATASET_FOLDER
        self.watch_folder = WATCH_FOLDER
        self.stop_event = threading.Event()
        
    def stop(self):
        self.stop_event.set()

    def run(self):
        logging.info("Simulating real-time data")

        for filename in os.listdir(self.dataset_folder):
            file_path = os.path.join(self.dataset_folder, filename)
            if os.path.isfile(file_path):  # Ensure we're copying files, not directories
                self.copy_to_watch_folder(file_path)
                time.sleep(10)  # Simulate a 10-second delay between file copies

    def copy_to_watch_folder(self, file_path):
        try:
            shutil.copy(file_path, self.watch_folder)
            logging.info(f"Copied {os.path.basename(file_path)} to {self.watch_folder}")
        except Exception as e:
            logging.error(f"Error copying {file_path}: {e}")
