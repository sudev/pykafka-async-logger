import logging
import time 
import sys
sys.path.append('../src')
import KafkaHandler as kl

logger = logging.getLogger('test_application')
logger.setLevel(logging.DEBUG)

KAFKA_WRONG_HOST = ''
# Lets give wrong kafka url and try what happens 
handler = kl.KafkaLoggingHandler(hosts_list= KAFKA_WRONG_HOST, topic= "testLogger", batch_size=100, key="Hello")

logger.addHandler(handler)

latency = []
# Log some messages
for i in range(200):
    t = time.time()
    logger.info('i = %d' % i)
    logger.debug('i = %d' % i)
time.sleep(20)
