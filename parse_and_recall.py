
from typing import Optional,List
"""
    Parse Data
"""


def retrieve_relevant_data(version_id: int, segment_id: Optional[int]):
    version_id_index, segment_id_index = 0, 1  # maybe change it later to CONSTS (in consts.py)
    record_id_index = 0

    # ToDo: maybe later take the for loops and put them in the same function
    #  decorator and then pass the values to the function calls

    # predicts_data == list of PredictionsData objects
    predictions_using_the_version_id = []
    if segment_id:
        for row in predicts_data:
            if row[version_id_index] == version_id and row[segment_id_index] == segment_id:
                predictions_using_the_version_id.append(
                    PredictionsData(version_id=row[0], segment_id=row[1], record_id=row[2], prediction_value=row[3]))
    else:
        for row in predicts_data:
            if row[version_id_index] == version_id:
                predictions_using_the_version_id.append(ActualData(record_id=row[0], actual_value=row[1]))

    # getting all the relevant record_ids from the predicts collected related to the version_id inserted by the request of the client
    record_ids_of_predicts = [prediction_data.record_id for prediction_data in predictions_using_the_version_id]

    actual_data_holding_these_record_ids = []
    for row in actual_data:
        if row[record_id_index] in record_ids_of_predicts:
            actual_data_holding_these_record_ids.append(row)

    true_positives = find_true_positives(predicts=predictions_using_the_version_id,
                                         real_data=actual_data_holding_these_record_ids)

    false_negatives = find_false_negatives(predicts=predictions_using_the_version_id,
                                           real_data=actual_data_holding_these_record_ids)


def find_true_positives(predicts: List, real_data: List) -> List:
    true_postives = set()  # no doubled or repetitive/redundent data allowed
    prediction_index, actual_value_index = 3, 1
    for predict_record, real_record in zip(predicts, real_data):
        if predict_record.prediction_value == real_record.actual_value:
            true_postives.add(UnionedData(version_id=predict_record.version_id,
                                          segment_id=predict_record.segment_id,
                                          record_id=predict_record.record_id,
                                          prediction_value=predict_record.prediction_value,
                                          actual_value=real_record.actual_value))
    return true_postives

def find_false_negatives(predicts: List, real_data: List):
    pass


def calculate_recall():
    """
        recall function is a performance metric applied to a data retrieved from a collection.
        it checks the accuracy of a ML model that run over data and decides for true negatives and false positives (unfortunately).
        the easiest way to calculate recall is :

        true positives // correctly predicted as positive           -->
        ___________ divided by                                      -->  RECALL RESULT
        total actual positives // true positives + false negatives  -->
    """
