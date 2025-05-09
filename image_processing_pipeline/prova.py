import tensorflow as tf
import numpy as np
model = tf.keras.models.load_model('binary_classification_model_0505.keras')
pred = model.predict(np.random.rand(1, 60, 60, 3))
