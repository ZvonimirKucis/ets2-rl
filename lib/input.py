from pyvjoy import pyvjoy
from config import config
from lib import util

class Input():
    def __init__(self):
        print("Setting joystick...")
        self.joystick = pyvjoy.VJoyDevice(1)
        self.joystick.reset()
        self.joystick.set_axis(pyvjoy.HID_USAGE_X, config.MAX_AXIS//2)
        self.joystick.set_axis(pyvjoy.HID_USAGE_Y, config.MIN_AXIS)
        self.joystick.set_axis(pyvjoy.HID_USAGE_Z, config.MIN_AXIS)
        print("Done")

    def _convert_output(self, network_output):
        k = config.MAX_AXIS/2
        joystick_input = -k * network_output + k
        return int(joystick_input)

    def send_input(self, wheel_output, brake_output, acc_output):
        wheel_axis = self._convert_output(-util.clip(wheel_output))
        brake_axis = self._convert_output(util.clip(brake_output))
        acc_axis = self._convert_output(util.clip(acc_output))

        self.joystick.data.wAxisX = wheel_axis
        self.joystick.data.wAxisZ = brake_axis
        self.joystick.data.wAxisY = acc_axis