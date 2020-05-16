"""Example Kafka consumer."""
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

user_topic = app.topic(USER_TOPIC)
cleaned_user_topic = app.topic(CLEANED_USER_TOPIC, internal=True, partitions=1)

counts = app.Table('user_activity_count',
                   partitions=1,
                   key_type=str,
                   default=int).tumbling(timedelta(minutes=1),
                                         expires=timedelta(minutes=5),
                                         key_index=False)


@app.agent(sink=[cleaned_user_topic])
async def publish_cleaned_message(stream):
    async for message in stream:
        yield message


@app.agent(user_topic, sink=[publish_cleaned_message])
async def clean_data(data):
    async for d in data:
        cleaned_data = perform_full_clean(d)
        yield cleaned_data


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
            print(
                f'{email} has now appeared multiple times'
            )
        # log derived data
        print("derived data: ", d)
