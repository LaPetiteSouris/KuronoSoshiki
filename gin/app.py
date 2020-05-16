# -*- coding: utf-8 -*-
"""Gin
Gin is a simple Kafka producer module. It loads data from given file
and publish to the topic set in environment variables.

You can also throttle the amount of messages coming through the topic
per second by changing TRANSACTIONS_PER_SECOND parameters.

"""
import os
from time import sleep
import json

from kafka import KafkaProducer
from loader import load_sample_data
# topic to be used
USER_TOPIC = os.environ.get('USER_TOPIC')
# Kafka broker
KAFKA_BROKER_URL = os.environ.get('KAFKA_BROKER_URL')
# Throttle messages per second
TRANSACTIONS_PER_SECOND = float(os.environ.get('TRANSACTIONS_PER_SECOND'))
SLEEP_TIME = 1 / TRANSACTIONS_PER_SECOND


if __name__ == '__main__':
    producer = KafkaProducer(
        bootstrap_servers=KAFKA_BROKER_URL,
        # Encode all values as JSON
        value_serializer=lambda value: json.dumps(value).encode(),
    )
    while True:
        # keep pushing data from sample JSON
        data = load_sample_data()
        for d in data:
            producer.send(USER_TOPIC, value=d)
            sleep(SLEEP_TIME)