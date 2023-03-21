from data_models import PredictionsData, ActualData, UnionedData
from typing import Optional, List, Dict

from kafka_producer import create_kafka_producer
from postgres_db import connect_and_retrieve_data_from_psotgres

"""
    Parse Data
"""


class ParseData:
    def __init__(self, segment_id, version_id, predicts_data, actual_data):
        self.segment_id = segment_id
        self.version_id = version_id
        self.predicts_data = predicts_data
        self.actual_data = actual_data
        self.predictions_using_the_version_id = {}
        self.actual_data_holding_these_record_ids = {}

    # ToDo: maybe later take the for loops  in the different functions and use it as a decorator

    def find_relevant_predictions(self):
        # predicts_data == dict of  {record_id : PredictionsData} key-val pares
        version_id_index, segment_id_index, record_id_index = 0, 1, 2  # maybe change it later to CONSTS and add into a dict (in consts.py)

        if self.segment_id:
            for row in self.predicts_data:
                if row[version_id_index] == self.version_id and row[segment_id_index] == self.segment_id:
                    self.predictions_using_the_version_id[row[2]] = (
                        PredictionsData(version_id=row[0], segment_id=row[1], record_id=row[2],
                                        prediction_value=row[3]))
        else:
            for row in self.predicts_data:
                if row[version_id_index] == self.version_id:
                    self.predictions_using_the_version_id[row[record_id_index]] = \
                        PredictionsData(version_id=row[0],
                                        segment_id=row[1],
                                        record_id=row[2],
                                        prediction_value=row[3])

    def find_relevant_actuals(self):
        record_id_index = 0

        # get the relevant record_ids from the predicts related to the version_id inserted by the request of the client
        record_ids_of_predicts = [prediction_data.record_id for prediction_data in
                                  self.predictions_using_the_version_id]
        # predicts_data == dict of  {record_id : PredictionsData} key-val pares
        for row in self.actual_data:
            if row[record_id_index] in record_ids_of_predicts:
                self.actual_data_holding_these_record_ids[row[record_id_index]] = (
                    ActualData(record_id=row[0], actual_value=row[1]))


def main_functionality(version_id: int, segment_id: Optional[int]):
    predicts_data, actual_data = connect_and_retrieve_data_from_psotgres()
    # init the main parser instance
    data_main_parser = ParseData(segment_id=segment_id, version_id=version_id, predicts_data=predicts_data,
                                 actual_data=actual_data)
    # run the 2 main functionalities in order to 'build' the relevant data sets
    data_main_parser.find_relevant_actuals()
    data_main_parser.find_relevant_predictions()

    true_positives = find_true_positives(predicts=data_main_parser.predictions_using_the_version_id,
                                         real_data=data_main_parser.actual_data_holding_these_record_ids)

    false_negatives = find_false_negatives(predicts=data_main_parser.predictions_using_the_version_id,
                                           real_data=data_main_parser.actual_data_holding_these_record_ids)

    total_positives = true_positives.union(false_negatives)

    recall_res = calculate_recall(true_positive=true_positives, total_actual_positive=total_positives)

    kafka_resp = create_kafka_producer(version_id=version_id, segment_id=segment_id, recall_result=recall_res)
    return kafka_resp


# ToDo : work on this function
def find_true_positives(predicts: Dict, real_data: Dict) -> set:
    true_positives = set()  # no doubled or repetitive/redundant data allowed

    for real_record_key in real_data.keys():
        if predicts[real_record_key] and real_data[real_record_key].prediction_value == predicts[
            real_record_key].actual_value:
            true_positives.add(UnionedData(version_id=predicts[real_record_key].version_id,
                                           segment_id=predicts[real_record_key].segment_id,
                                           record_id=predicts[real_record_key].record_id,
                                           prediction_value=predicts[real_record_key].prediction_value,
                                           actual_value=real_data[real_record_key].actual_value))
    return true_positives


# ToDo : work on this function
def find_false_negatives(predicts: Dict, real_data: Dict):
    false_negatives = set()  # no doubled or repetitive/redundant data allowed
    # for real_record_key in real_data.keys():
    #     if real_data[real_record_key] == predicts[real_record_key]:
    #         false_negatives.add(UnionedData(version_id=predicts[real_record_key].version_id,
    #                                         segment_id=predicts[real_record_key].segment_id,
    #                                         record_id=predicts[real_record_key].record_id,
    #                                         prediction_value=predicts[real_record_key].prediction_value,
    #                                         actual_value=real_data[real_record_key].actual_value))
    return false_negatives


# ToDo : work on this function
def calculate_recall(true_positive: set, total_actual_positive: set):
    """
        recall function is a performance metric applied to a data retrieved from a collection.
        it checks the accuracy of a ML model that run over data and decides for true negatives and false positives (unfortunately).
        the easiest way to calculate recall is :

        true positives // correctly predicted as positive           -->
        ___________ divided by                                      -->  RECALL RESULT
        total actual positives // true positives + false negatives  -->
    """
    recall_result = len(true_positive) // len(total_actual_positive)
    return recall_result
