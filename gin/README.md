# Gin
![Alt text](gin.jpg?raw=false "Gin")

Gin is a simple Kafka producer module. It loads data from given file
and publish to the topic set in environment variables.

You can also throttle the amount of messages coming through the topic
per second by changing TRANSACTIONS_PER_SECOND parameters.

The sample JSON message to publish:

```json
{"id":1,"first_name":"Barthel","last_name":"Kittel","email":"bkittel0@printfriendly.com","gender":"Male","ip_address":"130.187.82.195","date":"06/05/2018","country":"france"}
```
