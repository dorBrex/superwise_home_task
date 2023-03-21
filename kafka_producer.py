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


def create_kafka_producer(version_id: int, segment_id: int, recall_result: int):
    record_metadata = None

    producer = KafkaProducer(bootstrap_servers=[f"{conf['kafka_hostname']}:{conf['kafka_port']}"])

    kafka_ans = producer.send(conf['kafka_topic'], build_kafka_event(version_id=version_id, segment_id=segment_id,
                                                                     recall_func_results=recall_result))
    try:
        record_metadata = kafka_ans.get(timeout=10)
    except KafkaError:
        # log.exception()
        pass
    if record_metadata:
        print(record_metadata)
    return kafka_ans
