import psycopg2
from environs import Env


def connect():
    env = Env()
    env.read_env()
    return psycopg2.connect(
        dbname=env('dbname'),
        user=env('user'),
        password=env('password'),
        host=env('host'),
        port=env('port')
    )


connection = connect()
