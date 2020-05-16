# Kafka Data Quality Control

[![Kafka](https://img.shields.io/badge/streaming_platform-kafka-black.svg?style=flat-square)](https://kafka.apache.org)
[![Docker Images](https://img.shields.io/badge/docker_images-confluent-orange.svg?style=flat-square)](https://github.com/confluentinc/cp-docker-images)
[![Python](https://img.shields.io/badge/python-3.5+-blue.svg?style=flat-square)](https://www.python.org)

This is the implementation of my small blogpost: [A simple Data Quality Control for Streaming Service]().

Inspired by the article written here
[Building A Streaming Fraud Detection System With Kafka And Python](https://florimond.dev/blog/articles/2018/09/building-a-streaming-fraud-detection-system-with-kafka-and-python/)

The codebase for Kafka/Zookeeper stack ithes taken from the same blog post, as the author has done a brilliant work of puting the whole Kafka stack togheter in `docker-compse`. Many thanks to this tremendous effort, which allows my work to be implemented much easier.

## Install

This fraud detection system is fully containerised. You will need [Docker](https://docs.docker.com/install/) and [Docker Compose](https://docs.docker.com/compose/) to run it.

You simply need to create a Docker network called `kafka-network` to enable communication between the Kafka cluster and the apps:

```bash
$ docker network create kafka-network
```

All set!

## Quickstart

- Spin up the local single-node Kafka cluster (will run in the background):

```bash
$ docker-compose -f docker-compose.kafka.yml up -d
```

- Check the cluster is up and running (wait for "started" to show up):

```bash
$ docker-compose -f docker-compose.kafka.yml logs -f broker | grep "started"
```

- Start the stack, including `gin`, `vodka` and `bourbon`. Summazie

```
gin: Kafka producer, take the sample JSON file and simulate a coming of stream

vodka: cleaning service. Clean data and re-publish to a new topic. It also calculate sever data
stats on the flight.

bourbon: data quality watchdog. It calculates data stats from raw data
```
NOTE:  Only `bourbon` and `vodka` print out
their log. `gin` produces message to Kafka silently.

```bash
$ docker-compose up
```

## Usage

Show a stream of transactions in the topic `T` (optionally add `--from-beginning`):

```bash
$ docker-compose -f docker-compose.kafka.yml exec broker kafka-console-consumer --bootstrap-server localhost:9092 --topic T
```

Topics:

- `streaming.user_activity`: raw generated user event
- `derivedstream.cleaned_user_events`: user event cleaned by `vodka`
- `derivedstream.quality_user_activity`: quality control , publish by `bourbon`

Example transaction message:

```json
{"id":1,"first_name":"Barthel","last_name":"Kittel","email":"bkittel0@printfriendly.com","gender":"Male","ip_address":"130.187.82.195","date":"06/05/2018","country":"france"}
```

## Teardown

To stop the transaction generator and fraud detector:

```bash
$ docker-compose down
```

To stop the Kafka cluster (use `down`  instead to also remove contents of the topics):

```bash
$ docker-compose -f docker-compose.kafka.yml stop
```

To remove the Docker network:

```bash
$ docker network rm kafka-network
```
