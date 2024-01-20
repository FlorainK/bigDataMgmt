import faust
import json
from confluent_kafka.schema_registry.avro import AvroDeserializer
from confluent_kafka.serialization import StringDeserializer, SerializationContext, MessageField
from confluent_kafka.schema_registry import SchemaRegistryClient

def main():
    with open("../config.json") as json_file:
        config = json.load(json_file)

    kafka_server = config["kafka_server"]
    topic = config["kafka_topic"]
    schema_regestry_conf = config["schema_regestry_conf"]

    app = faust.App(
        "processing",
        broker=kafka_server,
    )
    app.topic(topic)

    schema_registry_client = SchemaRegistryClient(schema_regestry_conf)
    avro_deserializer = AvroDeserializer(
        schema_registry_client=schema_registry_client
    )

    @app.agent(topic)

    async def process(stream):
        async for event in stream:
            value = avro_deserializer(event.value(), SerializationContext(topic, MessageField.VALUE))
            print(value)
    app.main()

if __name__ == "__main__":
    main()