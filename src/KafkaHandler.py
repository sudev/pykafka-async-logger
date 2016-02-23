from pykafka import KafkaClient
import logging
import Queue
import socket


class KafkaHandler(logging.Handler):
    """Kafka logger handler attempts to write python logs directly
    into specified kafka topic instead of writing them into file.
    """

    def __init__(self, backup_file, hosts_list, topic, batch_size):
        logging.Handler.__init__(self)
        # Backup log file for errors
        self.fail_fh = open(backup_file, 'w')
        kafka_client = KafkaClient(hosts_list)
        topic = kafka_client.topics[topic]
        self.key = bytes(str(socket.gethostname()))
        self.producer = topic.get_producer(
            delivery_reports=True,
            min_queued_messages=batch_size,
            max_queued_messages=batch_size * 1000,
            linger_ms=15000,
            block_on_queue_full=False)
        self.count = 0

    def emit(self, record):
        """ This method receives logs as parameter record through 
        logging framework, send them to Kafka Cluster
        """
        # drop kafka logging to avoid infinite recursion
        if record.name == 'kafka':
            return
        try:
            # use default formatting, this should be overiden by goibibo buckter format
            msg = self.format(record)
            self.producer.produce(msg, partition_key=self.key)
            # Check on delivery reports
            self.count += 1
            if self.count > (self.batch_size * 2):
                self.check_delivery()
                self.count = 0
        except AttributeError:
            self.write_backup("Kafka Error!")
            self.write_backup(msg)
            pass
        except (KeyboardInterrupt, SystemExit):
            raise
        except:
            # Log erros due queue full
            self.write_backup(msg)
            self.handleError(record)

    def check_delivery(self):
        """Checks the delivery reports from Kafka producer,
        failed reported will be written to backup file.
        """
        while True:
            try:
                msg, exc = self.producer.get_delivery_report(block=False)
                if exc is not None:
                    self.write_backup(msg)
                    self.write_backup(repr(exc))
                    # Some alert action here maybe mail
            except Queue.Empty:
                break

    def write_backup(self, msg):
        self.fail_fh.write(msg +"\n")

    def close(self):
        self.fail_fh.close()
        self.producer.stop()
        logging.Handler.close(self)
