"""
ORM models for stage area PostgreSQL DB.
"""
from peewee import (
    CharField,
    DateField,
    FloatField,
    IntegerField,
    Model,
    PostgresqlDatabase)

import settings as config


POSTGRES_HOST = config.DATABASE['HOST']
POSTGRES_PORT = int(config.DATABASE['PORT'])
POSTGRES_DATABASE = config.DATABASE['DATABASE']
POSTGRES_USER = config.DATABASE['USER']
POSTGRES_PASSWORD = config.DATABASE['PASSWORD']

db_handle = PostgresqlDatabase(database=POSTGRES_DATABASE,
                               host=POSTGRES_HOST,
                               port=POSTGRES_PORT,
                               user=POSTGRES_USER,
                               password=POSTGRES_PASSWORD)


class BaseModel(Model):
    class Meta:
        database = db_handle


class Transactions(BaseModel):
    id_transaction = IntegerField(primary_key=True)
    id_account = IntegerField()
    transaction_type = CharField(max_length=255)
    transaction_date = DateField()
    transaction_amount = FloatField()

    class Meta:
        db_table = 'transactions_fct'
        schema = 'stage'
        order_by = ('transaction_date',)
        id = 'id_transaction'


class Accounts(BaseModel):
    id_account = IntegerField(primary_key=True)
    id_person = IntegerField()
    account_type = CharField(max_length=16)

    class Meta:
        db_table = 'accounts_dim'
        schema = 'stage'
        id = 'id_account'


class Persons(BaseModel):
    id_person = IntegerField(primary_key=True)
    name = CharField(max_length=128)
    surname = CharField(max_length=128)
    zip = CharField(max_length=16)
    city = CharField(max_length=64)
    country = CharField(max_length=64)
    email = CharField(max_length=512)
    phone_number = CharField(max_length=16)
    birth_date = DateField()

    class Meta:
        db_table = 'persons_dim'
        schema = 'stage'
        id = 'id_person'
