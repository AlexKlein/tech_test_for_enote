"""
Util for creating db tables.
"""
import os

from common import postgres_wrapper


def commands_launcher(sql_file, conn):
    sql_commands = sql_file.split(';')

    for command in sql_commands:

        if len(command.strip()) > 0:
            conn.execute(raw_sql=command)

    conn.execute(raw_sql='commit')


def start_up():
    connection = postgres_wrapper.PostgresWrapper()

    for path, dirs, files in os.walk(os.path.dirname(os.getcwd())):

        if path.find('migrations') > 0:

            for f in files:
                full_path = os.path.join(path, f)

                with open(full_path, 'r', encoding='UTF-8') as file:
                    commands_launcher(file.read(), connection)
