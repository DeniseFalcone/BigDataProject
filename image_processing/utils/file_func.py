import os
import shutil
import logging

# Load environment variables
# Folder to watch for new files
FOLDER_TO_WATCH = os.getenv("FOLDER_TO_WATCH")
#FOLDER_TO_WATCH = "data\imageserver"
FOLDER_TO_WATCH = os.path.realpath(FOLDER_TO_WATCH)
# Folder containing the dataset to copy in WATCH_FOLDER
DATASET_FOLDER = os.getenv("DATASET_FOLDER")
#DATASET_FOLDER = "data\dataset"
DATASET_FOLDER = os.path.realpath(DATASET_FOLDER)

def copy_to_watch_folder(file_path):
        try:
            shutil.copy(file_path, FOLDER_TO_WATCH)
            #logging.info(f"Copied {os.path.basename(file_path)} in {FOLDER_TO_WATCH}")
        except Exception as e:
            logging.error(f"Error copying {file_path}: {e}")

def move_file(src_path=None, dest_path=None):
    if src_path is None or not os.path.exists(src_path):
        logging.error(f"Source path does not exist: {src_path}")
        return
    if dest_path is None:
        logging.error(f"Destination path does not exist: {dest_path}")
        return
    try:
        shutil.move(src_path, dest_path)
        #logging.info(f"Moved file in {FOLDER_TO_WATCH}")
    except Exception as e:
        logging.error(f"Error moving file: {e}")

