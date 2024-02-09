import json, time, random
import paho.mqtt.client as mqtt
from kafka import KafkaProducer
from kafka.admin import KafkaAdminClient, NewTopic

def main():
    with open('../config.json') as json_file:
        config = json.load(json_file)

    kafka_configs = config['kafka_configs']

    admin_client = KafkaAdminClient(bootstrap_servers=kafka_configs['kafka_server'])
    if kafka_configs['topic_name'] not in admin_client.list_topics():
        admin_client.create_topics(new_topics = [NewTopic(name=kafka_configs['topic_name'], num_partitions=kafka_configs['partitions'], replication_factor=1)])
        print('topic created')
    kafka_producer = KafkaProducer(bootstrap_servers=kafka_configs['kafka_server'])

    i = 0
    while True:
        kafka_producer.send(kafka_configs['topic_name'],value = json.dumps({'fin':'floriansAuto', 'zeit': int(time.time()), 'geschwindigkeit': random.randint(5,50)}).encode('utf-8'))
        kafka_producer.flush()
        time.sleep(10)
        i += 1
        if i % 10 == 0: print(f'Sent {i} messages')


if __name__ == '__main__':
    main()