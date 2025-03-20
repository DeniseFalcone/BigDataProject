import shutil
import os
import time
import config

#print("Transfering Files...")

for filename in os.listdir(config.DATASET_FOLDER):
    f = os.path.join(config.DATASET_FOLDER, filename)
    shutil.copy(f,config.IMAGESERVER_FOLDER)
    time.sleep(3)