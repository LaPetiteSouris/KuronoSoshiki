# Vodka

![Alt text](vodka.jpg?raw=true "vodka")


Vodka is the a Faust (https://github.com/robinhood/faust) worker

It contains 3 Faust agents

1. Clean the raw message

2. Sink the cleaned message to a new Kafka topic

3. Subscribe to the topic contained cleaned data and calculate
some data statistics over a window of time.


![Alt text](vodka_diag.jpg?raw=true "vodka")