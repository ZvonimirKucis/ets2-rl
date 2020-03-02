import win32gui
import re
import numpy as np 
from scipy import misc, ndimage
from config import config
from lib import util, telemetryParser, input
import numpy as np 

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
        return util.make_screenshot(self.window_information['x'], 
                                            self.window_information['y'],
                                            self.window_information['w'],
                                            self.window_information['h'])

    def is_offence_shown(self, scr, threshold=0.7):
        offence_area = scr[config.CAPTION_Y1:config.CAPTION_Y2, config.CAPTION_X1:config.CAPTION_X2, :]
        _, _, score = util.template_match(needle=self.offence_ff_image, haystack=offence_area)
        return True if score >= threshold else False

    def is_damage_shown(self, scr, threshold=0.55):
        observed = scr[config.CAPTION_Y1:config.CAPTION_Y2, config.CAPTION_X1:config.CAPTION_X2, :]
        _, _, score = util.template_match(needle=self.damage_image, haystack=observed)
        return True if score >= threshold else False

    def is_reverse(self, scr=None, threshold=0.8):
        #observed = scr[config.REVERSE_Y1:config.REVERSE_Y2, config.REVERSE_X1:config.REVERSE_X2, :]
        #_, _, score = util.template_match(needle=self.reverse_image, haystack=observed)
        #return True if score >= threshold else False
        return telemetryParser.is_reverse()

    def is_wrong_way(self, scr, threshold=0.9):
        raise Exception('not implemented')

    def is_red_ligth(self, scr, treshold=0.9):
        raise Exception('not implemented')

    def is_speeding(self):
        return telemetryParser.is_speeding()

    def step(self):
        image = self.get_image()
        offence = self.is_offence_shown(np.array(image))
        damage = self.is_damage_shown(np.array(image))
        reverse = self.is_reverse(np.array(image))
        speed = telemetryParser.get_speed()
        speeding = self.is_speeding()

        state = [
            image,
            offence,
            damage,
            reverse,
            speeding,
            speed
        ]

        #print(f"\nspeed: {speed}")
        speed = speed if not reverse else -0.05 * speed
        #print(f"altered speed: {speed}")
        d = -50 if damage else 0
        o = -20 if offence else 0
        s = -40 if speeding else 0
        reward = speed + o + d + s

        #print(f"reward: {reward}, damage: {damage}, offence: {offence}, speeding: {speeding}")
        return state, reward*10

    def load_save_game(self):
        input.open_save_game_menu()
        nth_save = np.random.randint(0, config.RELOAD_MAX_SAVEGAME_NUMBER)
        input.load_game(nth_save)

    def toggle_lights(self):
        input.toggle_lights()
        
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