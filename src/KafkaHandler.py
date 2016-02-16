from pykafka import KafkaClient
import logging


class KafkaLoggingHandler(logging.Handler):

    def __init__(self, hosts_list, topic, batch_size, key=None):
        logging.Handler.__init__(self)
        self.kafka_client = KafkaClient(hosts_list)
        self.topic = self.kafka_client.topics[topic]
        self.key = bytes(key)
        self.producer = self.topic.get_producer() 

    def emit(self, record):
        # drop kafka logging to avoid infinite recursion
        # Or should I write them to a file ? (Grr.. there are too many of them too, so ignore) 
        if record.name ==  'kafka':
            return
        try:
            # use default formatting, this can be overiden by goibibo buckter format
            msg = self.format(record)
            msg = bytes(msg)
            # Keyed messages should be produced when ordering of message is important
            self.producer.produce(msg, partition_key= self.key)
        except (KeyboardInterrupt, SystemExit):
            raise
        except:
            self.handleError(record)

    def close(self):
        self.producer.stop()
        logging.Handler.close(self)
