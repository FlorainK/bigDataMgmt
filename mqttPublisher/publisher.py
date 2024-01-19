import paho.mqtt.client as mqtt
import time
import json
import random



def main():
    broker_address = "broker.hivemq.com"
    client = mqtt.Client(client_id= "awerufabnsd2342SF", clean_session = False)

    client.connect(broker_address)

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