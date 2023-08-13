from enum import Enum
from peewee import Model, AutoField, CharField, Proxy, ForeignKeyField


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


class TaskState(str, Enum):
    PROCESSING = "PROCESSING"
    COMPLETED = "COMPLETED"


class Task(BaseModel):
    id = AutoField(primary_key=True)
    description = CharField(max_length=255)
    state = CharField(
        max_length=255,
        choices=[(state.value, state.name) for state in TaskState],
        default=TaskState.PROCESSING,
    )
    processing_user = ForeignKeyField(User)
