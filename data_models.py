from dataclasses import dataclass

"""
    DataClasses to hold the data from the tables in a "nice and neat" pythonic object
"""


@dataclass
class PredictionsData:
    version_id: int  # The version of the ML model
    segment_id: int  # Represent specific segment in the customer data
    record_id: str  # Unique key to identify the record -- used as PRIMARY KEY
    prediction_value: int  # The prediction \ inference that was made by the ML model


@dataclass
class ActualData:
    record_id: str  # Unique key to identify the record -- used as PRIMARY KEY
    actual_value: int  # The value that the model was trying to predict


@dataclass(unsafe_hash=True)
class UnionedData:
    version_id: int
    segment_id: int
    record_id: str
    prediction_value: int
    actual_value: int  # The value that the model was trying to predict
