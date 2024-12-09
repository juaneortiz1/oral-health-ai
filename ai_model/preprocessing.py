import numpy as np
import tensorflow as tf
from tensorflow.keras.preprocessing.image import ImageDataGenerator

def preprocess_images(image_directory):
    """Preprocess images for AI model training"""
    datagen = ImageDataGenerator(
        rescale=1./255,
        validation_split=0.2
    )
    return datagen
