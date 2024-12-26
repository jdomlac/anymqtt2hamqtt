import paho.mqtt.client as mqtt
import yaml

class HomeAssistantSingleton(type):
    """
    Singleton metaclass for HomeAssistant class
    """

    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            instance = super(HomeAssistantSingleton, cls).__call__(*args, **kwargs)
            cls._instances[cls] = instance
        return cls._instances[cls]
    
class HomeAssistant(metaclass=HomeAssistantSingleton):
    def __init__(self):
        with open('../config/config.yaml', 'r') as file:
            self.brokerconfig = yaml.safe_load(file)
            
        self.mqttc = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)