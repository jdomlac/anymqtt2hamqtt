import json

class my_custom_sensor:

    def on_message(unique_id, device_name, topic, payload, homeassistant):
        if topic.endswith("up"):
            payload_json = json.loads(payload.decode("utf-8"))
            temperature = payload_json["uplink_message"]["decoded_payload"]["temperature_0"]
            humidity = payload_json["uplink_message"]["decoded_payload"]["humidity_0"]
            homeassistant.publish(unique_id, json.dumps({"temperature": temperature, "humidity": humidity}))
        pass

    def on_downlink(unique_id, device_name, message, mqtt_handler):
        pass

    def get_discovery_payload(device, device_name):
        unique_id = device["unique_id"]
        ret_val = {
            "dev": {
                "ids": unique_id,
                "name": device_name,
                "mf": "RIS",
                "mdl": "CustomSensor",
            },
            "o": {
                "name": "anymqtt2hamqtt",
                "sw": "1.0",
            },
            "cmps": {
                f"{unique_id}_temperature": {
                    "p": "sensor",
                    "device_class": "temperature",
                    "unit_of_measurement": "°C",
                    "value_template": "{{ value_json.temperature }}",
                    "unique_id": f"{unique_id}_temperature",
                },
                f"{unique_id}_humidity": {
                    "p": "sensor",
                    "device_class": "humidity",
                    "unit_of_measurement": "%",
                    "value_template": "{{ value_json.humidity }}",
                    "unique_id": f"{unique_id}_humidity",
                },
            },
            "state_topic": f"anymqtt2hamqtt/{unique_id}/state",
            "qos": 2,
        }

        return json.dumps(ret_val)