import io
import json

import faust
from avro.io import DatumReader, BinaryDecoder

def main():
    with open("../config.json") as json_file:
        config = json.load(json_file)

    kafka_server = config["kafka_server"]
    topic_name = config["kafka_topic"]

    app = faust.App(
        "processing",
        broker=kafka_server,
    )
    topic = app.topic(topic_name, key_type=bytes, value_type=bytes)

    @app.agent(topic)
    async def process(stream):
        async for key, value in stream.items():
            key_reader = io.BytesIO(key)
            value_reader = io.BytesIO(value)

            key_decoder = BinaryDecoder(key_reader)
            value_decoder = BinaryDecoder(value_reader)

            key_reader = DatumReader()
            value_reader = DatumReader()

            key_data = key_reader.read(key_decoder)
            value_data = value_reader.read(value_decoder)

            print(key_data, value_data)
    app.main()

if __name__ == "__main__":
    main()