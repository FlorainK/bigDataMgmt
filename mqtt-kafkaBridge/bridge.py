import json
import paho.mqtt.client as mqtt
from kafka import KafkaProducer
from kafka.admin import KafkaAdminClient, NewTopic



def main():
    with open("../config.json") as json_file:
        config = json.load(json_file)

    kafka_configs = config["kafka_configs"]
    mqtt_broker_address = config["mqtt_broker_address"]
    mqtt_broker_uname = config["mqtt_username"]

    admin_client = KafkaAdminClient(bootstrap_servers=kafka_configs["kafka_server"])
    if kafka_configs["topic_name"] not in admin_client.list_topics():
        admin_client.create_topics(new_topics = [NewTopic(name=kafka_configs["topic_name"], num_partitions=kafka_configs["topic_name"], replication_factor=1)])
    kafka_producer = KafkaProducer(bootstrap_servers=kafka_configs["kafka_server"])


    def on_message(client, userdata, message):
        print("message received " ,str(message.payload.decode("utf-8")))
        kafka_producer.send(kafka_configs["topic_name"],value = str(message.payload.decode("utf-8")).encode('utf-8'))
        kafka_producer.flush()


    client = mqtt.Client(mqtt_broker_uname, clean_session=False)
    client.on_message=on_message
    client.connect(mqtt_broker_address)
    client.subscribe("DataMgmt", qos=1) 
    client.loop_forever()



if __name__ == "__main__":
    main()

