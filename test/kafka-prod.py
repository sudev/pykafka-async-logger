import logging
import pdb 
import sys
sys.path.append('../src')
import KafkaHandler as kl

logger = logging.getLogger('test_application')
logger.setLevel(logging.DEBUG)


KAFKA_HOST = '' 
# Add the log message handler to the logger
handler = kl.KafkaLoggingHandler(hosts_list= KAFKA_HOST, topic= "testLogger", batch_size=100, key="Hello")

logger.addHandler(handler)

# Log some messages
for i in range(200):
    t = time.time()
    logger.info('i = %d' % i)
    logger.debug('i = %d' % i)
# Async call need to sleep for a while for producer to run
time.sleep(20)
