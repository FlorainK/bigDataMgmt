from uuid import uuid4
from confluent_kafka import Producer
from confluent_kafka.serialization import StringSerializer, SerializationContext, MessageField
from confluent_kafka.schema_registry import SchemaRegistryClient
from confluent_kafka.schema_registry.avro import AvroSerializer
import paho.mqtt.client as mqtt


def main():
    mqtt_broker_address = "broker.hivemq.com"
    mqtt_broker_uname = "awerufabnsd2342SF"
    topic = "myTopic"
    schema_registry_url = "http://localhost:8083"
    kafka_server = "localhost:29092"

    schema_regestry_conf = {"url": schema_registry_url}
    schema_registry_client = SchemaRegistryClient(schema_regestry_conf)
    avro_serializer = AvroSerializer(
        schema_registry_client=schema_registry_client,
        schema_str='{"type": "record", "name": "myrecord", "fields": [{"name": "f1", "type": "string"}]}',
    )

    string_serializer = StringSerializer("utf_8")
    producer = Producer({"bootstrap.servers": kafka_server})

    def delivery_report(err, msg):
        if err is not None:
            print("Message delivery failed: {}".format(err))
        else:
            print("Message delivered to {} [{}]".format(msg.topic(), msg.partition()))

    def on_message(client, userdata, message):
        producer.poll(0.0)
        print("message received " ,str(message.payload.decode("utf-8")))
        try:
            data = {"f1": str(message.payload.decode("utf-8"))}
            producer.produce(
                topic=topic,
                on_delivery=delivery_report,
                key = string_serializer(str(uuid4()), MessageField.KEY),
                value= avro_serializer(data, SerializationContext(topic, MessageField.VALUE)),
                ),
        
        except Exception as e:
            print(e)
        producer.flush()	
            
    mqtt_client = mqtt.Client(mqtt_broker_uname, clean_session=False)
    mqtt_client.on_message= on_message
    mqtt_client.connect(mqtt_broker_address)
    mqtt_client.subscribe("DataMgmt", qos=1) 
    mqtt_client.loop_forever()

    producer.flush()

if __name__ == "__main__":
    main()