"""Produce fake transactions into a Kafka topic."""

import os
from time import sleep
import json

from kafka import KafkaProducer
from loader import load_sample_data

USER_TOPIC = os.environ.get('USER_TOPIC')
KAFKA_BROKER_URL = os.environ.get('KAFKA_BROKER_URL')
TRANSACTIONS_PER_SECOND = float(os.environ.get('TRANSACTIONS_PER_SECOND'))
SLEEP_TIME = 1 / TRANSACTIONS_PER_SECOND


if __name__ == '__main__':
    producer = KafkaProducer(
        bootstrap_servers=KAFKA_BROKER_URL,
        # Encode all values as JSON
        value_serializer=lambda value: json.dumps(value).encode(),
    )
    while True:
        data = load_sample_data()
        for d in data:
            producer.send(USER_TOPIC, value=d)
            sleep(SLEEP_TIME)