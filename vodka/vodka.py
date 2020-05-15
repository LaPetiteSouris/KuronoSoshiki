"""Example Kafka consumer."""
import os
import faust
import copy

KAFKA_BROKER_URL = os.environ.get('KAFKA_BROKER_URL', 'broker:9092')
USER_TOPIC = os.environ.get('USER_TOPIC')


app = faust.App(
    'vodka',
    broker=KAFKA_BROKER_URL,
    value_serializer='json',
    consumer_auto_offset_reset='latest'
)

user_topic = app.topic(USER_TOPIC)


@app.agent(user_topic)
async def clean_country(data):
    async for d in data:
        cleaned_data = copy.deepcopy(d)
        coutry_capital = cleaned_data.get("country", "").title()
        cleaned_data["country"] = coutry_capital
        print(cleaned_data)
        # clean countries
        # make sure starts with Captical letter
        