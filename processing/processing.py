import faust
import json

def main():
    with open("../config.json") as json_file:
        config = json.load(json_file)

    kafka_server = config["kafka_server"]
    topic = config["kafka_topic"]