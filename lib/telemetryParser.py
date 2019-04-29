import json, urllib.request
from config import config

def is_speeding():
    response = urllib.request.urlopen(config.TELEMETRY_URL)
    data = json.loads(response.read().decode('utf8'))

    data_truck = data['truck']
    data_navigation = data['navigation']

    return int(data_truck['speed']) > int(data_navigation['speedLimit'])