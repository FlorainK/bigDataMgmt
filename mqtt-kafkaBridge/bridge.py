from confluent_kafka import Producer
from confluent_kafka.serialization import StringSerializer, SerializationContext, MessageField
from confluent_kafka.schema_registry import SchemaRegistryClient
from confluent_kafka.schema_registry.avro import AvroSerializer


def main():
    topic = "myTopic"
    schema_registry_url = "http://localhost:8081"
    kafka_server = "localhost:9094"

    schema_registry_client = SchemaRegistryClient({"url": schema_registry_url})
    avro_serializer = AvroSerializer(
        schema_str='{"type": "record", "name": "myrecord", "fields": [{"name": "f1", "type": "string"}]}',
        schema_registry_client=schema_registry_client,
        to_dict=True,
    )

    producer = Producer({"bootstrap.servers": kafka_server})

    def delivery_report(err, msg):
        if err is not None:
            print("Message delivery failed: {}".format(err))
        else:
            print("Message delivered to {} [{}]".format(msg.topic(), msg.partition()))

    while True:
        data = {"f1": "value1"}
        producer.produce(
            topic=topic,
            value=data,
            on_delivery=delivery_report,
            value_serializer=lambda v: avro_serializer.encode_record_with_schema(
                topic=topic, record=v
            ),
        )
        producer.poll(0)
        producer.flush()