"""Example Kafka consumer."""
import os
import faust
from datetime import timedelta

KAFKA_BROKER_URL = os.environ.get('KAFKA_BROKER_URL', 'broker:9092')

CLEANED_USER_TOPIC = os.environ.get('CLEANED_USER_TOPIC')

app = faust.App('bourbon',
                broker=KAFKA_BROKER_URL,
                value_serializer='json',
                consumer_auto_offset_reset='latest')

cleaned_user_topic = app.topic(CLEANED_USER_TOPIC, internal=True, partitions=1)

counts = app.Table('user_activity_count',
                   partitions=1,
                   key_type=str,
                   default=int).tumbling(timedelta(minutes=1),
                                         expires=timedelta(minutes=5),
                                         key_index=False)


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
