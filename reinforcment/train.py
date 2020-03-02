import numpy as np
from lib import util, telemetryParser
from reinforcment import actions
from config import config
from progress.bar import Bar
import time


def _get_network_input(state, vInput, predict):
    image = np.array(state[0])
    image_input = []
    image_input.append(image)

    state_input = [int(i) for i in state[1:]]
    #state_input.append(telemetryParser.get_speed())
    for element in list(vInput.get_current_values()):
        state_input.append(float(element))
    state_input = np.array(state_input)
    
    state_array = []
    state_array.append(state_input)
    if predict:
        return [np.asarray(image_input), np.asarray(state_array)]
    return [image, state_input]

def get_batch(states, outputs):
    image_input = []
    state_array = []
    output_array = []

    for s in states:
        #print(s)
        image = np.array(s[0])
        image_input.append(image)

        state_input = [i for i in s[1][:]]
        state_input = np.array(state_input)
        state_array.append(state_input)

    for o in outputs:
        output_array.append(np.asarray(o))

    return [image_input, state_array,], [output_array]


def _send_input(action, vInput):
    old_values = list(vInput.get_current_values())
    chosen_action = actions.ACTIONS_V2[action]

    for i,value in enumerate(chosen_action):
        old_values[i] = old_values[i] + value
        old_values[i] = util.clip(old_values[i])

    #print(old_values)
    vInput.send_input(*old_values)

def _filter(vInput, etsWindow):
    old_values = list(vInput.get_current_values())
    old_values = [float(i) for i in old_values]

    if etsWindow.is_reverse() and old_values[1] < 0 and old_values[2] >= 0:
        vInput.send_input(old_values[0], -1, -1)
        time.sleep(0.1)
        vInput.send_input(old_values[0], -1, 1)
        time.sleep(0.1)
        vInput.send_input(old_values[0], -1, -1)
        time.sleep(0.1)
        vInput.send_input(old_values[0], -1, 1)
        time.sleep(0.1)

    if not etsWindow.is_reverse() and old_values[2] < 0 and old_values[1] >= 0:
        vInput.send_input(old_values[0], -1, -1)
        time.sleep(0.1)
        vInput.send_input(old_values[0], 1, -1)
        time.sleep(0.1)
        vInput.send_input(old_values[0], -1, -1)
        time.sleep(0.1)
        vInput.send_input(old_values[0], 1, -1)
        time.sleep(0.1)

    vInput.send_input(*old_values)


# now execute the q learning
def q_learning(etsWindow, model, vInput, y=config.GAMA, eps=config.EPSILON, decay_factor=config.DECAY_FACTOR):
    for i in range(config.EPISODES):
        state, _ = etsWindow.step()
        eps *= decay_factor
        print("Episode {} of {}".format(i + 1, config.EPISODES))
        bar = Bar('Processing', max=config.STEPS, suffix='%(index)d/%(max)d - %(eta)ds')
        count = 0
        speedCount = 0
        batchInput = []
        batchOutput = []
        batchSize = 0

        for _ in range(config.STEPS):
            # wait until game is not paused
            while telemetryParser.is_paused():
                pass
            
            #dark = util.is_image_dark(state[0])
            #ligthsOn = telemetryParser.lights_on()
            #if dark:
            #    if not ligthsOn[0]:
            #        etsWindow.toggle_lights()
            #    if not ligthsOn[1]:
            #        etsWindow.toggle_lights()
            #else:
            #    if ligthsOn[0] or ligthsOn[1]:
            #        etsWindow.toggle_lights()

            if telemetryParser.is_damage_high() or telemetryParser.is_fuel_low():
                etsWindow.load_save_game()
                print('Game loaded')
                state, _ = etsWindow.step()
                bar.next()
                continue
            
            if np.random.random() < eps:
                action = np.random.randint(0, config.NUMBER_OF_ACTIONS)
            else:
                network_input = _get_network_input(state, vInput, True)
                action = np.argmax(model.predict(network_input))

            #print(f"\naction: {action}")
            _send_input(action, vInput)
            _filter(vInput, etsWindow)
            new_state, reward = etsWindow.step()
            if new_state[5] > 0:
                speedCount +=1
            else:
                speedCount = 0
            if reward == 0:
                count += 1
            else:
                count = 0
            if count > 5:
                reward -= count
            reward += speedCount
            network_input = _get_network_input(new_state, vInput, True)
            target = reward  + y * np.max(model.predict(network_input))
            #print(f"reward {reward}")
            #print(f"target: {target}")

            network_input = _get_network_input(state, vInput, True)
            target_vec = model.predict(network_input)[0]
            #print(f"target_vec: {target_vec}")
            target_vec[action] = target
            #print(f"target_vec: {target_vec}")

            model.fit(network_input, target_vec.reshape(-1, config.NUMBER_OF_ACTIONS), batch_size=config.BATCH_SIZE, epochs=1, verbose=0)

            state = new_state
            bar.next()
        bar.finish()

        # save model
        if (i + 1) % 50 == 0:
            model_json = model.to_json()
            with open(config.MODELS_DIR + "model-" + str(i + 1) + ".json", "w") as json_file:
                json_file.write(model_json)
            model.save_weights(config.MODELS_DIR + "model-" + str(i + 1) + ".h5")
            print("Saved model to disk")

        vInput.reset()
        etsWindow.load_save_game()
        print('Game loaded')