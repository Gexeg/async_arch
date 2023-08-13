from settings import settings
from adapters.db.models import proxy_database, User, Task
from peewee import SqliteDatabase


def db_init():
    db = SqliteDatabase(settings.database_path)
    proxy_database.initialize(db)
    db.connect()

    db.create_tables([User, Task], safe=True)
    return db


database = db_init()
