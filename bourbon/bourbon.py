# -*- coding: utf-8 -*-
"""Bourbon
Bourbon is the a Faust (https://github.com/robinhood/faust) worker
Bourbon is the simplified version of a dedicated Data Quality Watchdog
It contains 3 Faust agents

1. Enforce Data Quality Control on the raw data
2. Sink the message indicating data quality in the new topic
3. Subscribe to the topic contained data quality message and log it out.
"""
import os
import faust
from datetime import timedelta

import data_quality_controller as controller

KAFKA_BROKER_URL = os.environ.get('KAFKA_BROKER_URL', 'broker:9092')
# raw data topic
USER_TOPIC = os.environ.get('USER_TOPIC') 
# topic contains data quality result
DATAQUALITY_TOPIC = os.environ.get('DATAQUALITY_TOPIC')

app = faust.App('bourbon',
                broker=KAFKA_BROKER_URL,
                value_serializer='json')

user_topic = app.topic(USER_TOPIC)
quality_topic = app.topic(DATAQUALITY_TOPIC, internal=True, partitions=1)

# Windows table , to calculate data quality metrics if needed
counts = app.Table('user_activity_count',
                   partitions=1,
                   key_type=str,
                   default=int).tumbling(timedelta(minutes=1),
                                         expires=timedelta(minutes=5),
                                         key_index=False)


# Agent to pubish data quality message
@app.agent(sink=[quality_topic])
async def publish_quality_message(stream):
    async for message in stream:
        yield message


# Agent to perform data quality check
@app.agent(user_topic, sink=[publish_quality_message])
async def perform_quality_check(data):
    async for d in data:
        # perform check
        check_res = controller.perform_full_check(d)
        yield check_res


# Agent to log the data quality message
# and potentially implement further data quality control
# i.e: stats calculation, alerts monitoring....etc
@app.agent(quality_topic)
async def gate_keeper(data):
    async for d in data:
        print("data quality enforced on message...")
        print(d)