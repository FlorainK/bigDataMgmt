import faust
import json

def main():
    with open("../config.json") as json_file:
        config = json.load(json_file)

    kafka_server = config["kafka_server"]
    topic = config["kafka_topic"]

    app = faust.App(
        "processing",
        broker=kafka_server,
    )
    app.topic(topic)

    @app.agent(topic)

    async def process(stream):
        async for event in stream:
            print(event)
    app.main()

if __name__ == "__main__":
    main()