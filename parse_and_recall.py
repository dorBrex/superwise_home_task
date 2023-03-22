from typing import Optional, List, Dict, Tuple

from consts import VERSION_ID_INDEX, SEGMENT_ID_INDEX, RECORD_ID_INDEX_IN_PREDICTS, NEGATIVE_RESULT, POSITIVE_RESULT
from data_models import PredictionsData, ActualData, UnionedData
from kafka_producer import create_kafka_producer
from postgres_db import connect_and_retrieve_data_from_psotgres

"""
    Parse Data
"""


class ParseData:
    def __init__(self, segment_id: int, version_id: int, predicts_data: List[Tuple[int, int, str, int]],
                 actual_data: List[Tuple[str, int]]):
        self.segment_id = int(segment_id)
        self.version_id = int(version_id)
        self.predicts_data = predicts_data
        self.actual_data = actual_data
        self.predictions_using_the_version_id = {}
        self.actual_data_holding_these_record_ids = {}

    # ToDo: maybe later take the for loops  in the different functions and use it as a decorator

    def find_relevant_predictions(self):
        # predicts_data == dict of  {record_id : PredictionsData} key-val pares

        if self.segment_id:
            for row in self.predicts_data:
                if row[VERSION_ID_INDEX] == self.version_id and row[SEGMENT_ID_INDEX] == self.segment_id:
                    self.predictions_using_the_version_id[row[2]] = (
                        PredictionsData(version_id=row[0], segment_id=row[1], record_id=row[2],
                                        prediction_value=row[3]))
        else:
            for row in self.predicts_data:
                if row[VERSION_ID_INDEX] == self.version_id:
                    self.predictions_using_the_version_id[row[RECORD_ID_INDEX_IN_PREDICTS]] = \
                        PredictionsData(version_id=row[0],
                                        segment_id=row[1],
                                        record_id=row[2],
                                        prediction_value=row[3])
            return self.predictions_using_the_version_id

    def find_relevant_actuals(self):
        record_id_index = 0

        # get the relevant record_ids from the predicts related to the version_id inserted by the request of the client
        record_ids_of_predicts = [prediction_data[RECORD_ID_INDEX_IN_PREDICTS] for prediction_data in
                                  self.predicts_data]
        # predicts_data == dict of  {record_id : PredictionsData} key-val pares
        for row in self.actual_data:
            if row[record_id_index] in record_ids_of_predicts:
                self.actual_data_holding_these_record_ids[row[record_id_index]] = (
                    ActualData(record_id=row[0], actual_value=row[1]))
        return self.actual_data_holding_these_record_ids


def main_functionality(version_id: int, segment_id: Optional[int] = None):
    predicts_data, actual_data = connect_and_retrieve_data_from_psotgres()
    # init the main parser instance
    data_main_parser = ParseData(segment_id=segment_id, version_id=version_id, predicts_data=predicts_data,
                                 actual_data=actual_data)
    # run the 2 main functionalities in order to 'build' the relevant data sets
    data_main_parser.find_relevant_actuals()
    data_main_parser.find_relevant_predictions()

    actuals = data_main_parser.actual_data_holding_these_record_ids
    predicts = data_main_parser.predictions_using_the_version_id

    true_positives = find_true_positives(predicts=predicts,
                                         actual_data=actuals)

    false_negatives = find_false_negatives(predicts=predicts,
                                           actual_data=actuals)

    recall_res = calculate_recall(true_positives=true_positives, false_negatives=false_negatives)
    recall_res = recall_res if recall_res else 0
    kafka_resp = create_kafka_producer(version_id=version_id, segment_id=segment_id, recall_result=recall_res)
    return kafka_resp


def find_true_positives(predicts: Dict, actual_data: Dict) -> set:
    true_positives = set()  # no doubled or repetitive/redundant data allowed

    for predicted_record_key in predicts.keys():
        # checking if actuals has the same record key in them, and if so - checking if the prediction of that
        # record is the same at the actual value received. if so - add to the true_positives set
        if actual_data[predicted_record_key] and \
                actual_data[predicted_record_key].actual_value == predicts[predicted_record_key].prediction_value:
            true_positives.add(UnionedData(version_id=predicts[predicted_record_key].version_id,
                                           segment_id=predicts[predicted_record_key].segment_id,
                                           record_id=predicts[predicted_record_key].record_id,
                                           prediction_value=predicts[predicted_record_key].prediction_value,
                                           actual_value=actual_data[predicted_record_key].actual_value))
    print(f"There are {len(true_positives)} true positive")
    return true_positives


def find_false_negatives(predicts: Dict, actual_data: Dict) -> set:
    false_negatives = set()  # no doubled or repetitive/redundant data allowed
    for predicted_record_key in predicts.keys():
        # checking which records predicted as negative (0) but are actually positive (1)
        if actual_data[predicted_record_key] and predicts[predicted_record_key].prediction_value == NEGATIVE_RESULT and \
                actual_data[predicted_record_key].actual_value == POSITIVE_RESULT:
            false_negatives.add(UnionedData(version_id=predicts[predicted_record_key].version_id,
                                            segment_id=predicts[predicted_record_key].segment_id,
                                            record_id=predicts[predicted_record_key].record_id,
                                            prediction_value=predicts[predicted_record_key].prediction_value,
                                            actual_value=actual_data[predicted_record_key].actual_value))
    print(f"There are {len(false_negatives)} false negatives")
    return false_negatives


def calculate_recall(true_positives: set, false_negatives: set):
    """
        recall function is a performance metric applied to a data retrieved from a collection.
        it checks the accuracy of ML models that run over data and check how many true positives there are from the whole data that is actually true.
        the easiest way to calculate recall is :

        true positives // correctly predicted as positive               -->
        ___________ divided by                                          -->  RECALL RESULT
        total actual positives // true positives union false negatives  -->
                                -false negative: wrongly accusing true data to be false/negative
    """
    union_tp_and_fn = true_positives.union(false_negatives)

    print(f"There are {len(union_tp_and_fn)} true positive and false negative in total")
    # print(union_tp_and_fn)

    if len(union_tp_and_fn) != 0:
        recall_result = len(true_positives) / len(union_tp_and_fn)
        print(recall_result)
        return recall_result
    return
