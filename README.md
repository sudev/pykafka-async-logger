# python-kafka-logger

A simple handler for python logger to push logs into Kafka instead of writting them to disk. 

The logging handler will write to Kafka in async batch using kafka-python.

### Issues:

* Current version writes to Kafka using a different thread, so if the parent thread who was creating the logs exits then the messages won't be send to Kafka. 
    - To overcome this issue we might have to use [pykafka](https://github.com/Parsely/pykafka), and block termination of thread until messages are sent

Basically a async version of https://github.com/taykey/python-kafka-logging 
