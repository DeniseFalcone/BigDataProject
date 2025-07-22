import os
import json
import logging
import multiprocessing
from PIL import Image
from kafka import KafkaConsumer
from pymongo import MongoClient
import utils.file_func as file_func



# Load environment variables

# Kafka variables
KAFKA_URL = os.getenv("KAFKA_URL")
KAFKA_TOPIC = os.getenv("KAFKA_PATH_TOPIC")

# DATA FOLDERS
TO_PROCESS_FOLDER = os.getenv("TO_PROCESS_FOLDER")
TO_PROCESS_FOLDER = os.path.realpath(TO_PROCESS_FOLDER)
PROCESSED_FOLDER = os.getenv("PROCESSED_FOLDER")
PROCESSED_FOLDER = os.path.realpath(PROCESSED_FOLDER)

# MONGODB variables
MONGO_URL = os.getenv("MONGO_URL")
MONGO_DB = os.getenv("MONGO_DB")
MONGO_COLLECTION = os.getenv("MONGO_METADATA_COLLECTION")

# Class to consume images from Kafka, classify them and saving metadata to MongoDB
class ImageProcessingConsumer(multiprocessing.Process):

    def __init__(self):

        # Logging configuration
        multiprocessing.Process.__init__(self)
        logging.basicConfig(
            format="%(asctime)s - %(levelname)s - %(message)s",
            level=logging.INFO,
            handlers=[logging.StreamHandler()],
            force=True
        )

        # Mongo Connection
        client = MongoClient(MONGO_URL)
        DB = client[MONGO_DB]
        self.collection = DB[MONGO_COLLECTION]
        logging.info(f"Connected to MongoDB: {MONGO_URL}, Database: {MONGO_DB}, Collection: {MONGO_COLLECTION}")

        # Kafka connection
        logging.info("Connecting consumer to Kafka...")
        self.consumer = KafkaConsumer(
            KAFKA_TOPIC,
            bootstrap_servers=KAFKA_URL,
            value_deserializer=lambda v: json.loads(v.decode("utf-8")),
            auto_offset_reset="earliest",
            group_id="get-images-paths-group",
            enable_auto_commit=True
        )

        logging.info(f"Connected to Kafka: {KAFKA_URL}, Topic: {KAFKA_TOPIC}")
        self.stop_event = multiprocessing.Event()


    def create_json(self, src_path, dst_path, timestamp):

        import utils.data_preprocessing as data_preprocessing 

        img_to_predict = data_preprocessing.preprocess_image(src_path)
        logging.info(f"Image {os.path.basename(src_path)} to predict shape: {img_to_predict.shape}")
        prediction = float(self.prediction_model.predict(img_to_predict)[0][0])
        
        img = Image.open(src_path)
        width, height = img.size
        img.close()

        if prediction > 0.8:
            pred = "Tumor"
        else:
            pred = "No Tumor"
        return {
            "file_name": os.path.basename(src_path),
            "file_path": dst_path,
            "image_dimensions": {
                "width": width,  
                "height": height
            },
            "image_size_bytes": os.path.getsize(src_path),
            "label": pred,             
            "prediction_score": prediction,
            "timestamp": timestamp
        }    

    def stop(self):
        self.stop_event.set()

    def run(self):

        import tensorflow as tf

        try:

            #logging.info("Consumer process started — loading model")
            self.prediction_model = tf.keras.models.load_model('model/binary_classification_model_0505.keras')
            logging.info("Model loaded successfully")

            for message in self.consumer:
                file_path = message.value.get("file_path")
                logging.info(f"[PID {os.getpid()}] Processing image {file_path}")
                dest_path = os.path.join(PROCESSED_FOLDER, os.path.basename(file_path))
                try: 
                    self.collection.insert_one(self.create_json(src_path=file_path, dst_path=dest_path, timestamp=message.timestamp))
                except Exception as e:
                    logging.error(f"Error processing image {file_path}: {e}")     

                #logging.info(f"Moving file from {file_path} to {dest_path}")
                file_func.move_file(src_path=file_path, dest_path=dest_path)
                
        except Exception as e:
            logging.error(f"Error: {e}")
            
        finally:
            self.consumer.close()
            logging.info("Consumer closed")