import tensorflow as tf

from keras.backend.tensorflow_backend import set_session
tf_config = tf.ConfigProto()
tf_config.gpu_options.allow_growth = True
set_session(tf.Session(config=tf_config))

import keras
from keras.layers import Dense, Flatten, Dropout, Input, concatenate
from keras.applications.mobilenet import MobileNet
from keras.models import Model
from keras import backend as K
from keras.models import model_from_json
from keras.utils.generic_utils import get_custom_objects
import numpy as np
from config import config

def custom_activation(x):
    return (K.identity(x) /100)

get_custom_objects().update({'custom_activation': custom_activation})

class QModel:
    def __init__(self, image_shape, number_of_actions, modelJSON=None, modelH5=None):
        if modelJSON and modelH5:
            self._load_model(modelJSON, modelH5)
        else:
            self._generateModel(image_shape, number_of_actions)

    def _load_model(self, modelJSON, modelH5):
        # load json and create model
        json_file = open(modelJSON, 'r')
        loaded_model_json = json_file.read()
        json_file.close()
        loaded_model = model_from_json(loaded_model_json)
        # load weights into new model
        loaded_model.load_weights(modelH5)
        print("Loaded model from disk")

        self.model = loaded_model
        self.model.compile(loss='mse', optimizer='adam', metrics=['mae'])

    def _generateModel(self, image_shape, number_of_actions):
        pretranied_model = MobileNet(weights='imagenet', include_top=False)
        #pretranied_model.summary()

        for i, layer in enumerate(pretranied_model.layers):
            if i < 50:
                layer.trainable = False
            else:
                layer.trainable = True
        
        nn_input = Input(shape=image_shape,name = 'image_input')
        pretranied_model_output = pretranied_model(nn_input)

        x = Flatten(name='flatten')(pretranied_model_output)
        x = Dense(128, activation='relu', name='fc1')(x)

        additional_input = Input(shape=(config.ADDITIONAL_INPUTS,), name= 'state_info')
        additional_info = Dense(16, activation='relu', name='ad_fc1')(additional_input)
        additional_info = Dense(16, activation='relu', name='ad_fc2')(additional_info)

        x = concatenate([x, additional_info])
        x = Dense(128, activation='relu', name='fc2')(x)
        x = Dense(number_of_actions, activation=custom_activation, name='predictions')(x)

        self.model = Model(inputs=[nn_input, additional_input], outputs=x)
        self.model.compile(loss='mse', optimizer='adam', metrics=['mae'])