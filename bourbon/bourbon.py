"""Example Kafka consumer."""
import os
import faust
from datetime import timedelta

import data_quality_controller as controller

KAFKA_BROKER_URL = os.environ.get('KAFKA_BROKER_URL', 'broker:9092')
USER_TOPIC = os.environ.get('USER_TOPIC')
DATAQUALITY_TOPIC = os.environ.get('DATAQUALITY_TOPIC')

app = faust.App('bourbon',
                broker=KAFKA_BROKER_URL,
                value_serializer='json')

user_topic = app.topic(USER_TOPIC)
quality_topic = app.topic(DATAQUALITY_TOPIC, internal=True, partitions=1)

counts = app.Table('user_activity_count',
                   partitions=1,
                   key_type=str,
                   default=int).tumbling(timedelta(minutes=1),
                                         expires=timedelta(minutes=5),
                                         key_index=False)


@app.agent(sink=[quality_topic])
async def publish_quality_message(stream):
    async for message in stream:
        yield message


@app.agent(user_topic, sink=[publish_quality_message])
async def perform_quality_check(data):
    async for d in data:
        # perform check
        check_res = controller.perform_full_check(d)
        yield check_res


@app.agent(quality_topic)
async def gate_keeper(data):
    async for d in data:
        print(d)