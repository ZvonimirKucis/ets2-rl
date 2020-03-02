STEP = 0.3
WHEEL_STEP = 0.01

#(wheel, brake, acc)
ACTIONS = [
    (0, 0, 0),
    (0, STEP, STEP),
    (0, STEP, -STEP),
    (0, -STEP, STEP),
    (0, -STEP, -STEP),
    (WHEEL_STEP, 0, STEP),
    (WHEEL_STEP, 0, -STEP),
    (-WHEEL_STEP, 0, STEP),
    (-WHEEL_STEP, 0, -STEP),
    (WHEEL_STEP, STEP, 0),
    (WHEEL_STEP, -STEP, 0),
    (-WHEEL_STEP, STEP, 0),
    (-WHEEL_STEP, -STEP, 0),
    (WHEEL_STEP, STEP, STEP),
    (-WHEEL_STEP, STEP, STEP),  
    (-WHEEL_STEP, -STEP, STEP),
    (-WHEEL_STEP, -STEP, -STEP),
    (WHEEL_STEP, -STEP, STEP),
    (WHEEL_STEP, -STEP, -STEP),
    (-WHEEL_STEP, STEP, -STEP),
    (WHEEL_STEP, STEP, -STEP),
    (0, 0, STEP),
    (0, 0, -STEP),
    (0, STEP, 0),
    (0, -STEP, 0),
    (WHEEL_STEP, 0, 0),
    (-WHEEL_STEP, 0, 0)
]

ACTIONS_V2 = [
    (0, STEP, -STEP), # S
    (0, -STEP, STEP), # W
    (-WHEEL_STEP, 0, 0), # A
    (WHEEL_STEP, 0, 0) # D
]