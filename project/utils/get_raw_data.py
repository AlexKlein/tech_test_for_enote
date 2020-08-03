"""
An ETL process for uploading CSV-files to a PostgreSQL DB.

"""
from os import getcwd
from os.path import join

import pandas as pd
import re


CSV_FILES_DIR_PATH = join(join(getcwd(), 'storage'), 'data')


def transform_data(data_set, date_filed, id_field) -> pd.DataFrame:
    data_set = data_set.dropna(subset=[id_field])
    data_set = data_set.replace({pd.np.nan: 'null'})

    if date_filed is not None:
        try:
            data_set[date_filed] = pd.to_datetime(data_set[date_filed], format='%m/%d/%y')
        except ValueError:
            for index, row in data_set.iterrows():
                date_value = row[date_filed]

                with_mon = re.search(r'\d{2}-\w{3}-\d{2}', date_value)
                with_m = re.search(r'\d{1,2}/\d{1,2}/\d{2}', date_value)

                if with_mon is not None:
                    row[date_filed] = pd.to_datetime(date_value, format='%d-%b-%y')
                elif with_m is not None:
                    row[date_filed] = pd.to_datetime(date_value, format='%m/%d/%y')

    return data_set


def insert_set(data_set, model_name) -> str:
    model_name.truncate_table()
    model_name.insert_many(data_set.to_dict(orient='records')).execute()

    return str(data_set.count()[0]) + ' rows inserted'


def upload_csv_files(model_name):

    if model_name._meta.table_name == 'transactions_fct':
        headers = ['id_transaction', 'id_account', 'transaction_type', 'transaction_date', 'transaction_amount']
        date_filed = 'transaction_date'
        file_name = 'BI_assignment_transaction.csv'
    elif model_name._meta.table_name == 'accounts_dim':
        headers = ['id_account', 'id_person', 'account_type']
        date_filed = None
        file_name = 'BI_assignment_account.csv'
    else:
        headers = ['id_person', 'name', 'surname', 'zip', 'city', 'country', 'email', 'phone_number', 'birth_date']
        date_filed = 'birth_date'
        file_name = 'BI_assignment_person.csv'

    data_set = pd.read_csv(join(CSV_FILES_DIR_PATH, file_name),
                           verbose=True,
                           warn_bad_lines=True,
                           error_bad_lines=False,
                           skiprows=1,
                           sep=',',
                           names=headers)

    data_set = transform_data(data_set, date_filed, model_name._meta.id)
    return insert_set(data_set, model_name)


def start_up(model_name):
    return upload_csv_files(model_name)
