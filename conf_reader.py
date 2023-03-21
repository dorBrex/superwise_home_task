import configparser
import os

current_folder = os.path.dirname(os.path.abspath(__file__))
ini_file = os.path.join(current_folder, 'configurations.ini')


def read_ini(ini_file):
    config = configparser.ConfigParser()
    config.read(ini_file)

    # Postgres DB connection parameters
    db_type = config['POSTGRES']['DB_TYPE']
    db_hostname = config['POSTGRES']['HOSTNAME']
    db_port = config['POSTGRES']['PORT']
    db_username = config['POSTGRES']['USER']
    db_password = config['POSTGRES']['PSW']
    db_name = config['POSTGRES']['DB']

    # Kafka connection parameters
    kafka_hostname = config['KAFKA']['HOSTNAME']
    kafka_port = config['KAFKA']['PORT']
    kafka_topic = config['KAFKA']['TOPIC']

    return {'db_type': db_type,
            'db_hostname': db_hostname,
            'db_port': db_port,
            'db_username': db_username,
            'db_password': db_password,
            'db_name': db_name,
            'kafka_hostname': kafka_hostname,
            'kafka_port': kafka_port,
            'kafka_topic': kafka_topic,
            }


conf = read_ini(ini_file)
