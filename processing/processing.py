import json, datetime
import faust


def main():
    with open("../config.json") as json_file:
        config = json.load(json_file)

    kafka_configs = config["kafka_configs"]

    app = faust.App(
        "processing",
        broker=kafka_configs["kafka_server"],
        topic_partitions=8
    )
    topic = app.topic(kafka_configs["topic_name"], partitions=kafka_configs["partitions"], internal = True)
    speed_table = app.Table("speed_table", default = int).tumbling(60)


    @app.agent(topic)
    async def process(stream):
        async for value in stream:
            print(f"Received value: {value}")
            speed_table['sum'] += value['geschwindigkeit']
            speed_table['count'] += 1

            print(f"Current sum: {speed_table['sum'].value()}, count: {speed_table['count'].value()}")
    app.main()

if __name__ == "__main__":
    main()