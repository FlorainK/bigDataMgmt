from uuid import uuid4
from confluent_kafka import Producer
from confluent_kafka.serialization import StringSerializer, SerializationContext, MessageField
from confluent_kafka.schema_registry import SchemaRegistryClient
from confluent_kafka.schema_registry.avro import AvroSerializer


def main():
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

    while True:
        producer.poll(0.0)
        try:
            data = {"f1": "value1"}
            producer.produce(
                topic=topic,
                on_delivery=delivery_report,
                key = string_serializer(str(uuid4()), MessageField.KEY),
                value= avro_serializer(data, SerializationContext(topic, MessageField.VALUE)),
                ),
            
        except KeyboardInterrupt:
            break
        except Exception as e:
            print(e)
            continue

    producer.flush()

if __name__ == "__main__":
    main()