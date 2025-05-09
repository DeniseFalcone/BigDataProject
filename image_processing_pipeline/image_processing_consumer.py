import os
import json
import logging
import multiprocessing
os.environ["CUDA_VISIBLE_DEVICES"] = "-1"
from kafka import KafkaConsumer
import keras
import utils.file_func as file_func
import utils.data_preprocessing as data_preprocessing

# Load environment variables
# Kafka variables
KAFKA_URL = os.getenv("KAFKA_URL")
KAFKA_TOPIC = os.getenv("KAFKA_PATH_TOPIC")
# DATA FOLDERS
TO_PROCESS_FOLDER = os.getenv("TO_PROCESS_FOLDER")
TO_PROCESS_FOLDER = os.path.realpath(TO_PROCESS_FOLDER)
PROCESSED_FOLDER = os.getenv("PROCESSED_FOLDER")
PROCESSED_FOLDER = os.path.realpath(PROCESSED_FOLDER)


class ImageProcessingConsumer(multiprocessing.Process):

    def __init__(self):
        multiprocessing.Process.__init__(self)
        # Logging configuration
        logging.basicConfig(
            format="%(asctime)s - %(levelname)s - %(message)s",
            level=logging.INFO,
            handlers=[logging.StreamHandler()],
            force=True
        )
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
        self.prediction_model = keras.models.load_model("model/binary_classification_model_0505.keras")
        logging.info("Model loaded successfully")
        self.stop_event = multiprocessing.Event()

    def stop(self):
        self.stop_event.set()

    def run(self):
        try: 
            for message in self.consumer:
                file_path = message.value.get("file_path")
                dest_path = os.path.join(PROCESSED_FOLDER, os.path.basename(file_path))
                try:
                    img_to_predict = data_preprocessing.preprocess_image(file_path)
                    logging.info(f"Image {os.path.basename(file_path)} to predict shape: {img_to_predict.shape}")
                    pred = self.prediction_model.predict(img_to_predict)
                    if pred[0][0] > 0.8:
                        pred = "Tumor"
                    else:
                        pred = "No Tumor"
                    logging.info(f"Prediction for image {os.path.basename(file_path)}: {pred}")
                except Exception as e:
                    logging.error(f"Error processing image {file_path}: {e}")
                    continue
                logging.info(f"Moving file from {file_path} to {dest_path}")
                file_func.move_file(src_path=file_path, dest_path=dest_path)
        except Exception as e:
            logging.error(f"Error: {e}")
        finally:
            self.consumer.close()
            logging.info("Consumer closed")