import os

# telemetry server url
TELEMETRY_URL = "http://10.5.1.82:25555/api/ets2/telemetry"

# joystick mac and min value
MAX_AXIS = 32768
MIN_AXIS = 0

# region of interest for template match
REVERSE_X1 = 1070
REVERSE_X2 = 1100
REVERSE_Y1 = 500
REVERSE_Y2 = 530

CAPTION_X1 = 1050
CAPTION_X2 = 1200
CAPTION_Y1 = 570
CAPTION_Y2 = 620

MAIN_DIR = os.path.dirname(__file__) + "/../"

# Directory of an example image from an offence message.
OFFENCE_FF_IMAGE = os.path.join(MAIN_DIR, "images/offence_ff.png")
# Directory of an example image from a damage message (XX% damage).
DAMAGE_IMAGE = os.path.join(MAIN_DIR, "images/damage.png")
# Directory of an example image showing and activated reverse gear.
REVERSE_IMAGE = os.path.join(MAIN_DIR, "images/reverse.png")

# min and maximum direct reward range, used for computing bins
MIN_REWARD = -100
MAX_REWARD = 100

# keys for pause and quickload to use
KEY_PAUSE = "F1"
KEY_QUICKLOAD = "F11"

# Number of savegames to use during training. If set to N, the AI will
# load a random one of the first N savegames during reinforcement learning.
# (This happens many times during the training.)
RELOAD_MAX_SAVEGAME_NUMBER = 6
