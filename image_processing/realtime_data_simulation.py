import shutil
import os
import time
import logging
import threading
import random
import utils.file_func as file_func

# Load environment variables

# Folder to watch for new files
FOLDER_TO_WATCH = os.getenv("FOLDER_TO_WATCH")
FOLDER_TO_WATCH = os.path.realpath(FOLDER_TO_WATCH)

# Folder containing the dataset to copy in WATCH_FOLDER
DATASET_FOLDER = os.getenv("DATASET_FOLDER")
DATASET_FOLDER = os.path.realpath(DATASET_FOLDER)

# Real-time data simulator to copy files from DATASET_FOLDER to FOLDER_TO_WATCH
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

        #5-minute delay to make the consumer model ready to consume the data
        #time.sleep(300)

        img_lst = os.listdir(DATASET_FOLDER)

        # Shuffle the list of files to simulate randomness
        random.shuffle(img_lst) 

        for filename in img_lst:
            
            file_path = os.path.join(DATASET_FOLDER, filename)
            dest_path = os.path.join(FOLDER_TO_WATCH, filename)

            if os.path.isfile(file_path): 

                file_func.move_file(src_path=file_path, dest_path=dest_path)
                
                # Simulate a 10-second delay between file copies
                time.sleep(10)  

    
