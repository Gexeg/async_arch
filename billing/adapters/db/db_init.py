import os
from settings import settings
from adapters.db.models import proxy_database, User, Task, Transaction, UserAccount
from peewee import CharField
from playhouse.sqlite_ext import SqliteExtDatabase
from playhouse.migrate import SqliteMigrator, migrate


def task_migration(migrator: SqliteMigrator):
    migrate(migrator.add_column("task", "title", CharField(max_length=255, null=True)))


def db_init():
    db = SqliteExtDatabase(settings.database_path)
    proxy_database.initialize(db)
    db.connect()

    db.create_tables([User, Task, Transaction, UserAccount], safe=True)
    return db


database = db_init()
# в реальном коде нужно было бы придуматьс истему миграций или\и взять Alembic.
# migrator = SqliteMigrator(database)
# task_migration(migrator)
