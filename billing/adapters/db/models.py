import datetime
from enum import Enum
from peewee import (
    Model,
    AutoField,
    CharField,
    Proxy,
    ForeignKeyField,
    IntegerField,
    DateTimeField,
)
from playhouse.sqlite_ext import JSONField

proxy_database = Proxy()


class BaseModel(Model):
    class Meta:
        database = proxy_database


class User(BaseModel):
    id = AutoField(primary_key=True)
    public_id = CharField(max_length=255, unique=True)
    email = CharField(max_length=255)
    name = CharField(max_length=255)
    role = CharField(max_length=50)


class Task(BaseModel):
    id = AutoField(primary_key=True)
    public_id = CharField(max_length=255, unique=True)
    description = CharField(max_length=255)
    state = CharField(max_length=50)
    assign_cost = IntegerField()
    reward = IntegerField()
    processing_user = ForeignKeyField(User)


class TransactionType(str, Enum):
    task_assigned = "task_assigned"
    task_completed = "task_completed"


class Transaction(BaseModel):
    id = AutoField(primary_key=True)
    user_id = ForeignKeyField(User)
    transaction_type = CharField(
        max_length=50, choices=[(type.value, type.name) for type in TransactionType]
    )
    amount = IntegerField()
    data = JSONField()
    created = DateTimeField(default=datetime.datetime.now())


class UserAccount(BaseModel):
    id = AutoField(primary_key=True)
    user_id = ForeignKeyField(User)
    amount = IntegerField()
    created = DateTimeField(null=False)
