from lib import telemetryParser
import time
while True:
    print(telemetryParser.get_speed())
    print(int(telemetryParser.get_speed()))
    time.sleep(2)