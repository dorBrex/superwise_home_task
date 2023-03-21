from kafka import KafkaProducer
from kafka.errors import KafkaError

from conf_reader import conf

"""
    kafka producer logic
"""

kafka_hostname = conf['kafka_hostname']
kafka_port = conf['kafka_port']
kafka_topic = conf['kafka_topic']


def build_kafka_event(version_id, segment_id, recall_func_results):
    kafka_event_format = {'version_id': version_id,
                          'segment_id': segment_id,
                          'recall': recall_func_results}
    return kafka_event_format


producer = KafkaProducer(bootstrap_servers=[f"{conf['kafka_hostname']}:{conf['kafka_port']}"])
# Asynchronous by default
future = producer.send(conf['kafka_topic'], b'raw_bytes')
# Block for 'synchronous' sends
try:
    record_metadata = future.get(timeout=10)
except KafkaError:
    # Decide what to do if produce request failed...
    # log.exception()
    pass
