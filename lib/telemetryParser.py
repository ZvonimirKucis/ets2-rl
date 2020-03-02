import json, urllib.request
from config import config

def is_speeding():
    response = urllib.request.urlopen(config.TELEMETRY_URL)
    data = json.loads(response.read().decode('utf8'))

    data_truck = data['truck']
    data_navigation = data['navigation']

    if int(data_navigation['speedLimit']) == 0:
        return False
    return float(data_truck['speed']) > int(data_navigation['speedLimit'])

def get_speed():
    response = urllib.request.urlopen(config.TELEMETRY_URL)
    data = json.loads(response.read().decode('utf8'))

    data_truck = data['truck']

    return float(data_truck['speed'])

def is_paused():
    response = urllib.request.urlopen(config.TELEMETRY_URL)
    data = json.loads(response.read().decode('utf8'))

    game_data = data['game']

    return bool(game_data['paused'])

def is_fuel_low(treshold=0.15):
    response = urllib.request.urlopen(config.TELEMETRY_URL)
    data = json.loads(response.read().decode('utf8'))

    data_truck = data['truck']

    return True if float(data_truck['fuel']) / float(data_truck['fuelCapacity']) <= treshold else False

def is_damage_high(treshold=0.6):
    response = urllib.request.urlopen(config.TELEMETRY_URL)
    data = json.loads(response.read().decode('utf8'))

    data_truck = data['truck']

    if (data_truck['wearEngine'] >= treshold
        or data_truck['wearTransmission'] >= treshold
        or data_truck['wearCabin'] >= treshold
        or data_truck['wearChassis'] >= treshold
        or data_truck['wearWheels'] >= treshold):
        return True
    else:
        return False

def is_reverse():
    response = urllib.request.urlopen(config.TELEMETRY_URL)
    data = json.loads(response.read().decode('utf8'))

    data_truck = data['truck']

    return int(data_truck['gear']) <= 0

def lights_on():
    response = urllib.request.urlopen(config.TELEMETRY_URL)
    data = json.loads(response.read().decode('utf8'))

    data_truck = data['truck']

    return bool(data_truck['lightsParkingOn']), bool(data_truck['lightsBeamLowOn'])