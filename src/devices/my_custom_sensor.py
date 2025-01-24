import json
import base64

temp_threshold = 25

class my_custom_sensor:

    def on_message(unique_id, device_name, topic, payload, homeassistant):
        if topic.endswith("up"):
            payload_json = json.loads(payload.decode("utf-8"))
            temperature = payload_json["uplink_message"]["decoded_payload"]["temperature_0"]
            humidity = payload_json["uplink_message"]["decoded_payload"]["relative_humidity_0"]
            digital = payload_json["uplink_message"]["decoded_payload"]["digital_out_0"]
            homeassistant.publish(unique_id, json.dumps({"temperature": temperature, "humidity": humidity, "alarm_state": digital}))
        pass

    def on_downlink(unique_id, device_name, message, mqtt_handler):
        global temp_threshold

        if temp_threshold is None:
            temp_threshold = 25

        topic = message.topic
        payload = message.payload.decode("utf-8")

        if topic.endswith("alarm_reset"):
            temp = temp_threshold*10
            data = "AC53" + temp.to_bytes(2, byteorder='big').hex() + "01"
            data = base64.b64encode(bytes.fromhex(data)).decode("utf-8")
            downlink_payload = {
                "end_device_ids": {
                    "device_id": unique_id,
                    "application_ids": {"application_id": "upvdisca-rakwireless-rak3172-app"}
                },
                "downlinks": [{"f_port": 15, "frm_payload": data, "priority": "NORMAL"}]
            }
            mqtt_handler.publish(device_name, f"/down/replace", json.dumps(downlink_payload))

        if topic.endswith("set_temp"):
            payload = message.payload.decode("utf-8")
            temp_threshold = int(payload)
            temp = temp_threshold*10
            data = "AC53" + temp.to_bytes(2, byteorder='big').hex() + "00"
            data = base64.b64encode(bytes.fromhex(data)).decode("utf-8")
            downlink_payload = {
                "end_device_ids": {
                    "device_id": unique_id,
                    "application_ids": {"application_id": "upvdisca-rakwireless-rak3172-app"}
                },
                "downlinks": [{"f_port": 15, "frm_payload": data, "priority": "NORMAL"}]
            }
            mqtt_handler.publish(device_name, f"/down/replace", json.dumps(downlink_payload))
        
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
            f"{unique_id}_button": {
                "p": "button",
                "device_class": "restart",
                "unique_id": f"{unique_id}_button",
                "command_topic": f"anymqtt2hamqtt/{unique_id}/alarm_reset",
            },
            f"{unique_id}_alarm": {
                "p": "sensor",
                "unit_of_measurement": "",
                "value_template": "{{ value_json.alarm_state }}",
                "unique_id": f"{unique_id}_alarm",
            },
            },
            "state_topic": f"anymqtt2hamqtt/{unique_id}/state",
            "qos": 2,
        }

        return json.dumps(ret_val)