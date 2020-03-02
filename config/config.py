import os

# training parameters
EPISODES = 500
STEPS = 1000
BATCH_SIZE = 2
EPSILON = 0
DECAY_FACTOR = 0.999
GAMA = 0.95

# telemetry server url
TELEMETRY_URL = "http://10.5.1.82:25555/api/ets2/telemetry"

# number of given action in state
NUMBER_OF_ACTIONS = 4
# number of additional inputs
ADDITIONAL_INPUTS = 8

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

# Directory of models
MODELS_DIR = os.path.join(MAIN_DIR, "models/")

# Directory of an example image from an offence message.
OFFENCE_FF_IMAGE = os.path.join(MAIN_DIR, "images/offence_ff.png")
# Directory of an example image from a damage message (XX% damage).
DAMAGE_IMAGE = os.path.join(MAIN_DIR, "images/damage.png")
# Directory of an example image showing and activated reverse gear.
REVERSE_IMAGE = os.path.join(MAIN_DIR, "images/reverse.png")

# min and maximum direct reward range, used for computing bins
MIN_REWARD = -100
MAX_REWARD = 100

# Number of savegames to use during training. 
RELOAD_MAX_SAVEGAME_NUMBER = 4
