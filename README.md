# python-kafka-logger

A simple handler for python logger to push logs into Kafka instead of writting them to disk. 

The logging handler will write to Kafka in async batch using kafka-python.

Basically a async version of https://github.com/taykey/python-kafka-logging 
