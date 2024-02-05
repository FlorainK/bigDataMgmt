import json, datetime, os
import faust
from slidingWindow import SlidingWindow
import psycopg2

def main():
    with open("../config.json") as json_file:
        config = json.load(json_file)

    kafka_configs = config["kafka_configs"]
    
    app = faust.App(
        "processing",
        broker=kafka_configs["kafka_server"],
        topic_partitions= kafka_configs["partitions"]
    )
    topic = app.topic(kafka_configs["topic_name"], 
                      partitions=kafka_configs["partitions"],
                      value_type=Car)
    

    speed_sliding_window = SlidingWindow(5, 1)

    postgres_password = os.environ['POSTGRES_PASSWORD']
    postgres_user = os.environ['POSTGRES_USER']

    conn = psycopg2.connect(
        host="localhost",
        database="postgres",
        user=postgres_user,
        password=postgres_password
    )


    
    @app.agent(topic)
    async def process(stream):
        async for value in stream:
            speed_sliding_window.add(value.geschwindigkeit)
            print(f"Sliding Window: {speed_sliding_window.window}\nAverage: {speed_sliding_window.get_Average()}")
            
            # cur = conn.cursor()
            # cur.execute("INSERT INTO mqtt.messung (payload) VALUES (%s::jsonb)", (data,))
    app.main()

class Car(faust.Record):
    fin: str
    zeit: str
    geschwindigkeit: int

if __name__ == "__main__":
    main()