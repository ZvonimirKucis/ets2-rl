from pyvjoy import pyvjoy
import keyboard
from config import config
from lib import util
import time
import pyautogui

class Input():
    def __init__(self):
        print("Setting joystick...")
        self.joystick = pyvjoy.VJoyDevice(1)
        self.reset()
        print("Done")

    def _convert_output(self, network_output):
        k = config.MAX_AXIS/2
        joystick_input = -k * network_output + k
        return int(joystick_input)

    def reset(self):
        self.joystick.set_axis(pyvjoy.HID_USAGE_X, config.MAX_AXIS//2)
        self.joystick.set_axis(pyvjoy.HID_USAGE_Y, config.MIN_AXIS)
        self.joystick.set_axis(pyvjoy.HID_USAGE_Z, config.MIN_AXIS)
        self.joystick.update()

        self.old_wheel_value = 0
        self.old_brake_value = -1
        self.old_acc_value = -1

    def send_input(self, wheel_output, brake_output, acc_output):
        self.old_wheel_value = wheel_output
        self.old_brake_value = brake_output
        self.old_acc_value = acc_output

        wheel_axis = self._convert_output(-wheel_output)
        brake_axis = self._convert_output(brake_output)
        acc_axis = self._convert_output(acc_output)

        self.joystick.data.wAxisX = wheel_axis
        self.joystick.data.wAxisZ = brake_axis
        self.joystick.data.wAxisY = acc_axis

        self.joystick.update()

    def get_current_values(self):
        return [self.old_wheel_value, self.old_brake_value, self.old_acc_value]

def toggle_lights():
    keyboard.press_and_release('l')
    time.sleep(0.1)

def open_save_game_menu():
    keyboard.press_and_release('f11')
    time.sleep(2)
    
def load_game(nth_save):
    #click(270, 100)
    print("")
    i = 0
    while i < nth_save:
        print("Next savegame (switching to %d)" % (nth_save,))
        keyboard.press_and_release('down')
        time.sleep(1)
        i += 1
    time.sleep(2.0)
    for i in range(3):
        keyboard.press_and_release('return')
        time.sleep(1.0)
    time.sleep(3)

def click(x,y):
    pyautogui.moveTo(x, y)
    pyautogui.click(x, y)