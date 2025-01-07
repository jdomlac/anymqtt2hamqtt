import paho.mqtt.client as mqtt
import yaml
import threading
import device_handlers
import time

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
        self.mqttc.on_connect = self.on_connect
        self.mqttc.on_message = self.on_message

        if "broker_username" not in self.brokerconfig or self.brokerconfig["broker_username"] != '':
            self.mqttc.username_pw_set(username=self.brokerconfig["broker_username"], password=self.brokerconfig["broker_password"])

        self.thread = threading.Thread(target=self.run)
        self.thread.start()

        self.devices = {}

        self.broadcast_discovery_thread = threading.Thread(target=self.broadcast_discovery)
        self.broadcast_discovery_thread.start()

    def run(self):
        self.mqttc.connect(self.brokerconfig["broker_url"], self.brokerconfig["broker_port"], 60)
        self.mqttc.loop_forever()  

    def on_connect(self, client, userdata, flags, reason_code, properties):
        if reason_code.is_failure:
            print(f"Failed to connect: {reason_code}. Retrying...")
        else:
            print("Broker",self.brokerconfig["broker_url"],"succesfully connected")
            client.subscribe("$SYS/#")

    def on_message(self, client, userdata, message):
        topic = message.topic

    def broadcast_discovery(self):
        while True:
            for uuid in self.devices:
                device, mqtt_handler = self.devices[uuid]
                device_type = device["type"]
                device_handler = device_handlers.handlers_list[device_type]
                self.mqttc.publish(f"homeassistant/sensor/{uuid}/config", device_handler.get_discovery_payload(device))
                print("Broadcasted discovery for",device)
            time.sleep(5)

    def publish(self, unique_id, device_name, payload):
        pass

    def register_device(self, device, mqtt_handler):
        print("Registering device",device)
        self.devices[device["unique_id"]] = (device, mqtt_handler)