# pykafka-async-logger

A simple handler for python logger to push logs into Kafka instead of writting them to disk.

The logging handler will write to Kafka in async batch using [pykafka](https://github.com/Parsely/pykafka). Current implementation works well, but is not fault tolerant if kafka fails (Server not available, Leader not available) results in error/application crash.

### Todo:

* Logger fails when Kafka is down, need to tweak code such that Handler can be configured in runtime (If runtime change of handler is available!) else tweak to emit logs into file instead of pushing into Kafka.
* Write test cases and fix issues where Kafka client connection is already established and then fails(Leader not available for partition and other Kafka errors)
* Introduce snappy compression of messages.
* Configure pykafka to use [librdkafka](https://github.com/edenhill/librdkafka), this will effectively better performance a lot, especially while using compression.

Inspired from https://github.com/taykey/python-kafka-logging, python-kafka async implementation is here in this [branch](https://github.com/sudev/pykafka-async-logger/tree/python-kafka)

### Get the project

1. Clone the git repository   
    ```shell
    git clone https://github.com/taykey/python-kafka-logging/
    ```
1. Create a new virtualenv  
    ```shell
    virtualenv python_kafka_logging
    ```
1. Install project's requirements  
    ```shell
    python_kafka_logging/bin/pip install -r requirements.txt
    ```
