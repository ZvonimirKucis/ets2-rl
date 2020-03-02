import numpy as np
from lib import ets2Window
from lib.input import Input
from reinforcment.model import QModel
from reinforcment.train import q_learning
from config import config

#import argparse # parsing if train or drive
def display(np_image):
    from PIL import Image
    img = Image.fromarray(np_image, 'RGB')
    img.show()

def train():
    vjoy_input = Input()

    window = ets2Window.ETS2Window()
    print(window)

    image = window.get_image()
    np_image = np.array(image)
    model = QModel(np_image.shape, config.NUMBER_OF_ACTIONS, config.MODELS_DIR + "model.json", config.MODELS_DIR + "model.h5")
    model.model.summary()

    q_learning(window, model.model, vjoy_input)
        
    # TODO: wrong way, off road, game state, savegame loading
    # fatigue disabeld, gas disabeld


def drive():
    pass

train()