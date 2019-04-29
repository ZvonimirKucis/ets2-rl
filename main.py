import numpy as np
from lib import ets2Window
from lib.input import Input

#import argparse # parsing if train or drive
def display(np_image):
    from PIL import Image
    img = Image.fromarray(np_image, 'RGB')
    img.show()

def train():
    vjoy_input = Input()
    vjoy_input.send_input(1,1,1)
    window = ets2Window.ETS2Window()
    print(window)
    while True:
        image = window.get_image()
        np_image = np.array(image)

        if window.is_damage_shown(np_image):
            print("DAMAGE!!")
        if window.is_offence_shown(np_image):
            print("offence comited")
        if window.is_reverse(np_image):
            print("in reverse")
        if window.is_speeding():
            print("speeding...")
        
        # TODO: wrong way, off road, game state, savegame loading
        # fatigue disabeld, gas disabeld


def drive():
    pass

train()