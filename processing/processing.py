import json, datetime, os
import faust
from slidingWindow import SlidingWindow
import psycopg2
from car import Car

def main():
    with open('../config.json') as json_file:
        config = json.load(json_file)

    kafka_configs = config['kafka_configs']
    
    app = faust.App(
        'processing',
        broker=kafka_configs['kafka_server'],
        topic_partitions= kafka_configs['partitions']
    )
    topic = app.topic(kafka_configs['topic_name'], 
                      partitions=kafka_configs['partitions'],
                      value_type=Car)
    

    speed_sliding_window = SlidingWindow(5, 1)

    postgres_password = os.environ['POSTGRES_PASSWORD']
    postgres_user = os.environ['POSTGRES_USER']

    conn = psycopg2.connect(
        host='localhost',
        database='postgres',
        user=postgres_user,
        password=postgres_password
    )


    cur = conn.cursor()
    cur.execute('CREATE SCHEMA IF NOT EXISTS mqtt;')
    cur.execute('''CREATE TABLE IF NOT EXISTS mqtt.messung 
                (messung_id serial PRIMARY KEY, 
                payload jsonb not null,
                empfangen TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP);''')

    @app.agent(topic)
    async def process(stream):
        async for value in stream:
            last_value = speed_sliding_window.get_last_value() \
                if speed_sliding_window.get_last_value() \
                else value.geschwindigkeit
            
            speed_sliding_window.add(value.geschwindigkeit)
            value.durchschnittsgeschwindigkeit = speed_sliding_window.get_average()

            value.beschleunigung = value.geschwindigkeit - last_value
            
            if value.beschleunigung < -30: print('Warnung: starkes Bremsen erkannt')
            data_jsonS = value.to_json()

            cur = conn.cursor()
            cur.execute('INSERT INTO mqtt.messung (payload) VALUES (%s::jsonb)', 
                        (data_jsonS,))
            conn.commit()

    app.main()
    cur.close()


if __name__ == '__main__':
    main()