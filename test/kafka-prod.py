import logging
import pdb 
import time 
import numpy 
import sys
sys.path.append('../src')
import KafkaHandler as kl

logger = logging.getLogger('spam_application')
logger.setLevel(logging.DEBUG)

# Add the log message handler to the logger
handler = kl.KafkaLoggingHandler(hosts_list="10.70.46.67:9092", topic= "testLogger", batch_size=100, key="Hello")

logger.addHandler(handler)

latency = []
# Log some messages
for i in range(200):
    t = time.time()
    logger.info('i = %d' % i)
    logger.debug('i = %d' % i)
    latency.append(time.time() - t)

nl = numpy.array(latency)
print(numpy.mean(nl))
print(numpy.std(nl))
time.sleep(20)
