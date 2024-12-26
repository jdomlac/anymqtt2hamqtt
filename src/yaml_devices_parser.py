import yaml
import device_handlers
import uuid

def parse_yaml(file_path):
    with open(file_path, 'r') as file:
        data = yaml.safe_load(file)

    ret_data = {}

    for broker in data:
        
        if "url" not in data[broker] or data[broker]["url"] == '':
            print("Broker",broker,"URL is empty")
            continue

        if "port" not in data[broker] or data[broker]["port"] == '':
            data[broker]["port"] = 1883

        if "username" not in data[broker]:
            data[broker]["username"] = ''

        if "password" not in data[broker]:
            data[broker]["password"] = ''
        
        if "devices" not in data[broker]:
            print("No devices found for broker",broker)
            continue

        devices_to_remove = []

        for device in data[broker]["devices"]:

            if "topic" not in data[broker]["devices"][device] or data[broker]["devices"][device]["topic"] == '':
                print("No topic found for device",device,"in broker",broker)
                devices_to_remove.append(device)
                continue

            if "type" not in data[broker]["devices"][device] or data[broker]["devices"][device]["type"] == '':
                print("No type found for device",device,"in broker",broker)
                devices_to_remove.append(device)
                continue

            if data[broker]["devices"][device]["type"] not in device_handlers.handlers_list:
                print("No handler found for device",device,"in broker",broker)
                devices_to_remove.append(device)
                continue

            if "unique_id" not in data[broker]["devices"][device] or data[broker]["devices"][device]["unique_id"] == '':
                print("Generating unique_id for device",device,"in broker",broker)
                data[broker]["devices"][device]["unique_id"] = str(uuid.uuid4())
                #Add this to the yaml file
                with open(file_path, 'w') as file:
                    yaml.dump(data, file)

        for device in devices_to_remove:
            del data[broker]["devices"][device]

        if data[broker]["devices"] != {}:
            ret_data[broker] = data[broker]
        else:
            print("Ignoring broker",broker,"as no devices properly configured")

    return ret_data