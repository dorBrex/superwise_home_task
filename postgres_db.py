from typing import Tuple, List

from conf_reader import conf
import psycopg2

"""
    PostgressSQL Database
"""


def connect_and_retrieve_data_from_psotgres() -> Tuple[List, List]:
    # establishing the connection
    conn = psycopg2.connect(
        database=conf['db_name'],
        user=conf['db_username'],
        password=conf['db_password'],
        host=conf['db_hostname'],
        port=conf['db_port']
    )

    cursor = conn.cursor()

    cursor.execute(
        "SELECT * FROM Predictions")  # 200 rows of data in Predictions Table, each row looks like - (1, 1, 'A49E4E99156D', 0)
    predictions_table = cursor.fetchall()

    cursor.execute(
        "SELECT * FROM Actual")  # 1034 rows of data in Actual Table, each row looks like - ('A49E4E99156D', 0)
    actual_table = cursor.fetchall()

    # Closing the connection
    conn.close()
    return predictions_table, actual_table
