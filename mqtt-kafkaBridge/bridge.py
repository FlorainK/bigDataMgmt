import json
import io

import paho.mqtt.client as mqtt
from kafka import KafkaProducer
import avro.schema
from avro.datafile import DataFileWriter
from avro.io import DatumWriter


def main():
    with open("../config.json") as json_file:
        config = json.load(json_file)

    kafka_topic = config["kafka_topic"]
    kafka_server = config["kafka_server"]
    mqtt_broker_address = config["mqtt_broker_address"]
    mqtt_broker_uname = config["mqtt_username"]

    schema = avro.schema.parse(open("../avro_schema/schema.avsc", "rb").read())

    kafka_producer = KafkaProducer(bootstrap_servers=kafka_server)

    writer = DataFileWriter(open("../avro_schema/schema.avsc", "wb"), DatumWriter(), schema)

    def on_message(client, userdata, message):
        decoded_message = json.loads(message.payload.decode("utf-8"))
        print("message received " , decoded_message)

        writer.write(decoded_message, encoder)
        bytes_writer = io.BytesIO()
        encoder = avro.io.BinaryEncoder(bytes_writer)
        kafka_producer.send(kafka_topic, bytes_writer.getvalue())   
        kafka_producer.flush()


    client = mqtt.Client(mqtt_broker_uname, clean_session=False)
    client.on_message=on_message
    client.connect(mqtt_broker_address)
    client.subscribe("DataMgmt", qos=1) 
    client.loop_forever()



if __name__ == "__main__":
    main()

