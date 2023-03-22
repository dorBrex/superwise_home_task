from json import dumps

import kafka
from conf_reader import conf

"""
    kafka producer logic
"""

kafka_hostname = conf['kafka_hostname']
kafka_port = conf['kafka_port']
kafka_topic = conf['kafka_topic']


def build_kafka_event(version_id: int, segment_id: int, recall_func_results: float):
    kafka_event_format = {'Version_id': version_id,
                          'Segment_id': segment_id,
                          'Recall': recall_func_results}
    return kafka_event_format


def create_kafka_producer(version_id: int, segment_id: int, recall_result: float):
    producer = kafka.KafkaProducer(bootstrap_servers=[f"{conf['kafka_hostname']}:{conf['kafka_port']}"],
                                   value_serializer=lambda x: dumps(x).encode('utf-8'))
    recall_data = build_kafka_event(version_id=version_id, segment_id=segment_id, recall_func_results=recall_result)
    # producer.send('recall', recall_data)
    # sleep(3)
    record_metadata = None

    kafka_ans = producer.send(conf['kafka_topic'], recall_data)
    try:
        record_metadata = kafka_ans.get(timeout=5)
    except Exception as e:
        # log.exception(e)
        pass
    if record_metadata:
        # Successful result returns assigned partition and offset
        print(f"\n\nKafka's metadata response:\n "
              f"topic: {record_metadata.topic} \n "
              f"partition: {record_metadata.partition} \n "
              f"offset: {record_metadata.offset}")
    return kafka_ans
