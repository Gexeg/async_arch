from settings import settings
from adapters.db.models import proxy_database, User, Task
from peewee import SqliteDatabase
from playhouse.migrate import SqliteMigrator, migrate
from peewee import CharField


def db_init():
    db = SqliteDatabase(settings.database_path)
    proxy_database.initialize(db)
    db.connect()

    db.create_tables([User, Task], safe=True)
    return db


def task_migration(migrator: SqliteMigrator):
    migrate(migrator.add_column("task", "title", CharField(max_length=255, null=True)))


database = db_init()
# в реальном коде нужно было бы придуматьс истему миграций или\и взять Alembic.
# migrator = SqliteMigrator(database)
# task_migration(migrator)
