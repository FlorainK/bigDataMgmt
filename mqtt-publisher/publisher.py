import paho.mqtt.client as mqtt
import time
import json
import random



def main():
    with open("../config.json") as json_file:
        config = json.load(json_file)

    mqtt_broker_address = config["mqtt_broker_address"]
    mqtt_broker_uname = config["mqtt_username"]

    client = mqtt.Client(client_id= "mqtt_broker_uname", clean_session = False)
    client.connect(mqtt_broker_address)

    fin = "FloriansAuto"

    while True:
        zeit = int(time.time())
        geschwindigkeit = random.randint(0, 50)

        data = {
            "fin": fin,
            "zeit": zeit,
            "geschwindigkeit": geschwindigkeit
        }

        json_data = json.dumps(data)

        client.publish("DataMgmt", json_data, qos = 1)
        print("published: " + json_data)
        time.sleep(5)




if __name__ == "__main__":
    main()