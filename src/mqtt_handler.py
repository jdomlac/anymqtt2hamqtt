import paho.mqtt.client as mqtt
import device_handlers

class MqttHandler:
    def __init__(self,userconfig):

        self.broker_url = userconfig["url"]
        self.broker_port = userconfig["port"]
        self.broker_user = userconfig["username"]
        self.broker_pass = userconfig["password"]
        self.devices = userconfig["devices"]

        #Topic -> device, uuid mapping
        self.topic_device_mapping = {}
        for device in self.devices:
            self.topic_device_mapping[self.devices[device]["topic"]] = (device, self.devices[device]["unique_id"])

        self.mqttc = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
        self.mqttc.on_connect = self.on_connect
        self.mqttc.on_message = self.on_message

        if self.broker_user != '':
            self.mqttc.username_pw_set(username=self.broker_user, password=self.broker_pass)

    def run(self):
        self.mqttc.connect(self.broker_url, self.broker_port, 60)
        self.mqttc.loop_forever()

    def on_connect(self, client, userdata, flags, reason_code, properties):
        if reason_code.is_failure:
            print(f"Failed to connect: {reason_code}. Retrying...")
        else:
            print("Broker",self.broker_url,"succesfully connected")
            for device in self.devices:
                topic = self.devices[device]["topic"]
                print("Subscribing to topic",topic)
                client.subscribe(f"{topic}/#")

    def on_message(self, client, userdata, message):
        topic = message.topic
        print("Received message from topic",topic)
        