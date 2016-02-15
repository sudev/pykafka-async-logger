from kafka.client import KafkaClient
from kafka.producer import SimpleProducer, KeyedProducer
import logging


class KafkaLoggingHandler(logging.Handler):

    def __init__(self, hosts_list, topic, batch_size, key=None):
        logging.Handler.__init__(self)
        self.kafka_client = KafkaClient(hosts_list)
        self.key = key
        self.kafka_topic_name = topic
        if not key:
            self.producer = SimpleProducer(self.kafka_client, async=True, batch_send_every_n = batch_size)
        else:
            self.producer = KeyedProducer(self.kafka_client, async=True, batch_send_every_n = batch_size)

    def emit(self, record):
        # drop kafka logging to avoid infinite recursion
        # Or should I write them to a file ? (Grr.. there are too many of them too, so ignore) 
        if record.name == 'kafka':
            return
        try:
            # use default formatting
            msg = self.format(record)
            if isinstance(msg, unicode):
                msg = msg.encode("utf-8")
            # produce message
            if not self.key:
                # Keyed messages should be produced when ordering of message is important
                self.producer.send_messages(self.kafka_topic_name, msg)
            else:
                self.producer.send(self.kafka_topic_name, self.key, msg)
        except (KeyboardInterrupt, SystemExit):
            raise
        except:
            self.handleError(record)

    def close(self):
        self.producer.stop()
        logging.Handler.close(self)
