import win32gui
import re
import numpy as np 
from scipy import misc, ndimage
from config import config
from lib import screenshot, util, telemetryParser

class ETS2Window():
    def __init__(self):
        self.window_information = {}
        win32gui.EnumWindows(self._callback, self.window_information)
        if 'window_name' not in self.window_information.keys():
            raise Exception('ETS2 not running')

        self.offence_ff_image = ndimage.imread(config.OFFENCE_FF_IMAGE, mode="RGB")
        self.damage_image = ndimage.imread(config.DAMAGE_IMAGE, mode="RGB")
        self.reverse_image = ndimage.imread(config.REVERSE_IMAGE, mode="RGB")

    def get_image(self):
        return screenshot.make_screenshot(self.window_information['x'], 
                                          self.window_information['y'],
                                          self.window_information['w'],
                                          self.window_information['h'])

    def is_offence_shown(self, scr, threshold=0.7):
        x1 = 1050
        y1 = 570
        x2 = 1200
        y2 = 620
        offence_area = scr[config.CAPTION_Y1:config.CAPTION_Y2, config.CAPTION_X1:config.CAPTION_X2, :]
        _, _, score = util.template_match(needle=self.offence_ff_image, haystack=offence_area)
        return score >= threshold

    def is_damage_shown(self, scr, threshold=0.55):
        x1 = 1050
        y1 = 570
        x2 = 1200
        y2 = 620
        observed = scr[config.CAPTION_Y1:config.CAPTION_Y2, config.CAPTION_X1:config.CAPTION_X2, :]
        _, _, score = util.template_match(needle=self.damage_image, haystack=observed)
        return score >= threshold

    def is_reverse(self, scr, threshold=0.9):
        x1 = 1070
        y1 = 500
        x2 = 1100
        y2 = 530
        observed = scr[config.REVERSE_Y1:config.REVERSE_Y2, config.REVERSE_X1:config.REVERSE_X2, :]
        _, _, score = util.template_match(needle=self.reverse_image, haystack=observed)
        return score >= threshold

    def is_wrong_way(self, scr, threshold=0.9):
        raise Exception('not implemented')

    def is_red_ligth(self, scr, treshold=0.9):
        raise Exception('not implemented')

    def is_speeding(self):
        return telemetryParser.is_speeding()
        
    def _callback(self, hwnd, data):
        name = win32gui.GetWindowText(hwnd)
        if bool(re.search('Truck', name)):
            rect = win32gui.GetWindowRect(hwnd)
            w = rect[2] - rect[0]
            h = rect[3] - rect[1]
            if w < 200 or h < 100:
                return

            data['window_name'] = name
            data['x'] = rect[0]
            data['y'] = rect[1]
            data['w'] = w
            data['h'] = h

    def __str__(self):
        return str(self.window_information['window_name']) \
                + "\n\tLocation: x: " \
                + str(self.window_information['x']) \
                + ", y: " + str(self.window_information['y']) \
                + "\n\tSize: w: " \
                + str(self.window_information['w']) \
                + ", h: " + str(self.window_information['h'])