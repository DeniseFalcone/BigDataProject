import shutil
import os
import time
import logging
import threading

# Load environment variables
# Folder to watch for new files
WATCH_FOLDER = os.getenv("WATCH_FOLDER")
# Folder containing the dataset to copy in WATCH_FOLDER
DATA_FOLDER = os.getenv("DATASET_FOLDER")


class RealTimeDataSimulator(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        logging.basicConfig(
            format="%(asctime)s - %(levelname)s - %(message)s",
            level=logging.INFO,
            handlers=[logging.StreamHandler()],
            force=True
        )
        self.stop_event = threading.Event()
        
    def stop(self):
        self.stop_event.set()

    def run(self):
        logging.info("Simulating real-time data")
        for filename in os.listdir(DATA_FOLDER):
            file_path = os.path.join(DATA_FOLDER, filename)
            if os.path.isfile(file_path): 
                self.copy_to_watch_folder(file_path)
                # Simulate a 10-second delay between file copies
                time.sleep(10)  

    def copy_to_watch_folder(self, file_path):
        try:
            shutil.copy(file_path, WATCH_FOLDER)
            logging.info(f"Copied {os.path.basename(file_path)} to {WATCH_FOLDER}")
        except Exception as e:
            logging.error(f"Error copying {file_path}: {e}")
