# python-kafka-logger

A simple handler for python logger to push logs into Kafka instead of writting them to disk. 

The logging handler will write to Kafka in async batch using [pykafka](https://github.com/Parsely/pykafka). Current implementation works well, but is not fault tolerant if kafka fails (Server not available, Leader not available ..) ==> no logs.

### Todo:

* Logger fails when Kafka is down, need to tweak code such that Handler can be configured in runtime (If runtime change of handler is available!) else tweak to emit logs into file instead of pushing into Kafka.
* Write test case where Kafka client connection is already established and then fails(Leader not available for partition and other Kafka errors) 
* Introduce snappy compression of messages.
* Configure pykafka to use [librdkafka](https://github.com/edenhill/librdkafka), this will effectively better performance a lot, especially while using compression.

Inspired from https://github.com/taykey/python-kafka-logging 
