"""
Wrapper for PostgreSQL connection for easier creations DB sessions.
"""
import psycopg2

import settings as config


POSTGRES_HOST = config.DATABASE['HOST']
POSTGRES_PORT = int(config.DATABASE['PORT'])
POSTGRES_DATABASE = config.DATABASE['DATABASE']
POSTGRES_USER = config.DATABASE['USER']
POSTGRES_PASSWORD = config.DATABASE['PASSWORD']


class PostgresWrapper:
    def __init__(self):
        self.user = POSTGRES_USER
        self.password = POSTGRES_PASSWORD
        self.host = POSTGRES_HOST
        self.port = POSTGRES_PORT
        self.db_name = POSTGRES_DATABASE
        self._connection = None

    @property
    def connection(self):
        if self._connection is not None:
            return self._connection
        self._connection = psycopg2.connect(
            user=self.user,
            password=self.password,
            database=self.db_name,
            host=self.host,
            port=self.port)
        return self._connection

    @staticmethod
    def _data_to_dict(data: dict):
        result = dict()
        result['headers'] = [x.lower() for x in data['headers']]
        result = [dict(zip(result['headers'], x)) for x in data['data']]

        return result

    def execute(
            self,
            raw_sql: str,
            params: tuple = (),
    ):
        cursor = self.connection.cursor()

        try:
            cursor.execute(raw_sql, params)
        finally:
            cursor.close()

    def execute_many(
            self,
            raw_sql: str,
            data: list,
    ):
        cursor = self.connection.cursor()

        try:
            cursor.executemany(raw_sql, data)
        finally:
            cursor.close()

    def execute_query(
            self,
            raw_sql: str,
            params: dict = {},
            data_to_dict: bool = True
    ):
        cursor = self.connection.cursor()

        try:
            cursor.execute(raw_sql, params)
            headers = [x[0] for x in cursor.description]
            rows = cursor.fetchall()
            data = {'headers': headers, 'data': rows}

            if data_to_dict:
                data = self._data_to_dict(data)

            return data

        finally:
            cursor.close()

    def close(self):
        if self._connection is not None:
            self._connection.close()
            self._connection = None
