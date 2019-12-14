
from keras.models import load_model
import numpy as np
import argparse
import pickle
import cv2
import tensorflow as tf

class Predictor:

    def __init__(self, model_path, labels_path):
        self.labels_map = {
            'bones' : 'b',
            'boogers' : 's',
            'corn' : 'k',
            'curses' : 'c',
            'hearts' : 'h',
            'pee' : 'u',
            'poop' : 'p',
            'teeth' : 't',
            'wilds' : 'w'
        }
        self.model = load_model(model_path)
        self.model._make_predict_function()
        self.labels = pickle.loads(open(labels_path, "rb").read())

    def predict(self, image): # image data expected to come as a PIL image
        numpy_image = np.array(image)
        opencv_image = cv2.cvtColor(numpy_image, cv2.COLOR_RGB2BGR)
        opencv_image = cv2.resize(opencv_image, (32, 32)) # make sure it's the correct dimentions
        opencv_image = opencv_image.astype("float") / 255.0 # change color values from 0-255 to 0-1
        opencv_image = opencv_image.reshape((1, opencv_image.shape[0], opencv_image.shape[1], opencv_image.shape[2]))

        return self.labels_map[self.labels.classes_[self.model.predict(opencv_image).argmax(axis=1)[0]]] # return the label of the model's highest condfidence prediction and map the label to its associated letter