# -*- coding: utf-8 -*-
"""Vodka
Vodka is the a Faust (https://github.com/robinhood/faust) worker

It contains 3 Faust agents

1. Clean the raw message
2. Sink the cleaned message to a new Kafka topic
3. Subscribe to the topic contained cleaned data and calculate
some data statistics over a window of time.

"""
import os
import faust
from datetime import timedelta

from data_cleaner import perform_full_clean

KAFKA_BROKER_URL = os.environ.get('KAFKA_BROKER_URL', 'broker:9092')
USER_TOPIC = os.environ.get('USER_TOPIC')
CLEANED_USER_TOPIC = os.environ.get('CLEANED_USER_TOPIC')

app = faust.App('vodka',
                broker=KAFKA_BROKER_URL,
                value_serializer='json',
                consumer_auto_offset_reset='latest')

# raw data topic
user_topic = app.topic(USER_TOPIC)
# topic contains cleaned data
cleaned_user_topic = app.topic(CLEANED_USER_TOPIC, internal=True, partitions=1)

# Faust windowed table, serve as storage for
# statistics calculation
# refer to https://faust.readthedocs.io/en/latest/userguide/tables.html
counts = app.Table('user_activity_count',
                   partitions=1,
                   key_type=str,
                   default=int).tumbling(timedelta(minutes=1),
                                         expires=timedelta(minutes=5),
                                         key_index=False)


# Faust agent to publish the cleaned message
@app.agent(sink=[cleaned_user_topic])
async def publish_cleaned_message(stream):
    async for message in stream:
        yield message


# Faust agent to perform data cleaning
@app.agent(user_topic, sink=[publish_cleaned_message])
async def clean_data(data):
    async for d in data:
        cleaned_data = perform_full_clean(d)
        yield cleaned_data


# Faust agent to perform data stats calculation
@app.agent(cleaned_user_topic)
async def log_derived_data(data):
    async for d in data:
        # count country
        country = d["country"]
        counts[country] += 1

        print(f'{country} has now appeared {counts[country].value()} times')

        # count email address
        email = d["email"]
        counts[email] += 1
        if counts[email].value() >= 5:
            print(f'{email} has now appeared multiple times')
        # log derived data
        print("derived data: ", d)
