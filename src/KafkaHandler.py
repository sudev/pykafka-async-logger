from pykafka import KafkaClient
import logging
import socket


class KafkaLoggingHandler(logging.Handler):
    def __init__(self, hosts_list, topic, batch_size):
        """Kafka logger handler attempts to write python logs directly
        into specified kafka topic instead of writing them into file.
        """
        logging.Handler.__init__(self)
        self.kafka_client = KafkaClient(hosts_list)
        self.topic = self.kafka_client.topics[topic]
        self.key = bytes(socket.gethostname())
        self.producer = topic.get_producer(
            delivery_reports=True,
            min_queued_messages=batch_size,
            max_queued_messages=batch_size * 100,
            linger_ms=15000,
            block_on_queue_full=False)

    def emit(self, record):
        """ This method receives logs as parameter record through
        logging framework, send them to Kafka Cluster
        """
        # drop kafka logging to avoid infinite recursion
        # Or should I write them to a file ? (Grr.. there are too many of them too, so ignore)
        if record.name == 'kafka':
            return
        try:
            # use default formatting, this can be overiden by goibibo buckter format
            msg = self.format(record)
            msg = bytes(msg)
            # Keyed messages should be produced when ordering of message is important
            self.producer.produce(msg, partition_key=self.key)
        except (KeyboardInterrupt, SystemExit):
            raise
        except:
            self.handleError(record)

    def close(self):
        self.producer.stop()
        logging.Handler.close(self)
