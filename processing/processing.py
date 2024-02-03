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
    topic = app.topic(topic_name)

    @app.agent(topic)
    async def process(stream):
        async for value in stream:
            print(value)
    app.main()

if __name__ == "__main__":
    main()