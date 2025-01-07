from yaml_devices_parser import parse_yaml
from mqtt_handler import MqttHandler
import threading
from homeassistant import HomeAssistant

def main():
    userconfig = parse_yaml('../config/devices.yaml')
    mqtt_handlers = {}
    mqtt_threads = {}

    homeassistant = HomeAssistant()
    
    for broker in userconfig:
        mqtt_handlers[broker] = MqttHandler(userconfig[broker])
        mqtt_threads[broker] = threading.Thread(target=mqtt_handlers[broker].run)
        mqtt_threads[broker].start()

if __name__ == '__main__':
    main()