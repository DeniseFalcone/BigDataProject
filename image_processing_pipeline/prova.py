import tensorflow as tf
import numpy as np
import utils.data_preprocessing as data_preprocessing
import os

model = tf.keras.models.load_model('model/binary_classification_model_0505.keras')
#from data/to_process_images take an image and preprocess it
script_dir = os.path.dirname(os.path.abspath(__file__))
file_path = os.path.join(script_dir, "..", "data/to_process_images", "000000.png")
file_path = os.path.normpath(file_path)
print(file_path)

input = data_preprocessing.preprocess_image(file_path)
print("Image to predict shape: ", input.shape)

pred = model.predict(np.random.rand(1, 60, 60, 3))

print(pred)
