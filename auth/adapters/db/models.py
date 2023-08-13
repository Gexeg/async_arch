from enum import Enum
from peewee import Model, AutoField, CharField, Proxy


proxy_database = Proxy()


class BaseModel(Model):
    class Meta:
        database = proxy_database


class UserRole(str, Enum):
    ADMIN = "admin"
    WORKER = "worker"
    MANAGER = "manager"


class User(BaseModel):
    id = AutoField(primary_key=True)
    email = CharField(max_length=255)
    name = CharField(max_length=255)
    role = CharField(
        max_length=50, choices=[(role.value, role.name) for role in UserRole]
    )
    password_hash = CharField(max_length=255)
