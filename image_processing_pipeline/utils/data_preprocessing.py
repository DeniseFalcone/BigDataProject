from PIL import Image
import numpy as np
import logging


def crop_center(img_array: np.ndarray):
    height, width = img_array.shape[:2]
    new_width, new_height = 60, 60

    left = (width - new_width) // 2
    top = (height - new_height) // 2
    right = left + new_width
    bottom = top + new_height

    return img_array[top:bottom, left:right]


def load_img(img_path):
    img = Image.open(img_path)
    return np.array(img)
    

def normalize(x_array: np.ndarray):
  return x_array / 255.0


def preprocess_image(img_path):
    logging.info(f"Preprocessing image: {img_path}")
    img_array = load_img(img_path)
    logging.info(f"Image shape before cropping: {img_array.shape}")
    img_array = crop_center(img_array)
    logging.info(f"Image shape after cropping: {img_array.shape}")
    img_array = normalize(img_array)
    logging.info(f"Image shape after normalization: {img_array.shape}")
    return np.expand_dims(img_array, axis=0)
