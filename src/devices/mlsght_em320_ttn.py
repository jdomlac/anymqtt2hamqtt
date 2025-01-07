import json

class mlsght_em320_ttn:

    def on_message(unique_id, device_name, message):
        print(message)

    def on_downlink(unique_id, device_name, message, mqtt_handler):
        pass

    def get_discovery_payload(unique_id):
        ret_val = {
            "name": "EM320",
            "unique_id": unique_id,
            "state_topic": f"homeassistant/sensor/{unique_id}/state",
            "availability_topic": f"homeassistant/sensor/{unique_id}/availability",
            "payload_available": "online",
            "payload_not_available": "offline",
            "json_attributes_topic": f"homeassistant/sensor/{unique_id}/attributes",
            "unit_of_measurement": "W",
            "value_template": "{{ value_json.power }}"
        }

        return json.dumps(ret_val)