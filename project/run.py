"""
Entrypoint for the ETL process running.
"""
from time import sleep

from models import stage_models as models
from utils.db_migration import start_up as start_db
from utils.get_raw_data import start_up as get_raw_data


def check_data():
    if not models.Transactions.table_exists():
        start_db()


def delay_db():
    i = 1
    run_flag = 0
    while i <= 10 and run_flag != 1:
        try:
            models.db_handle.connect()
            run_flag = 1
            break
        except:
            sleep(i)
            i += 1

    if run_flag == 1:
        return 'DB started.'
    else:
        return 'DB didn\'t start.'


if __name__ == '__main__':
    print(delay_db())
    check_data()

    get_raw_data(models.Transactions)
    get_raw_data(models.Accounts)
    get_raw_data(models.Persons)
