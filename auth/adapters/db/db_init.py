from settings import settings
from db.models import proxy_database, User, UserRole
from utils.password import get_password_hash
from peewee import SqliteDatabase


def db_init():
    db = SqliteDatabase(settings.database_path)
    proxy_database.initialize(db)
    db.connect()

    db.create_tables([User], safe=True)
    if not User.select().exists():
        with db.atomic():
            User.create(
                name="Admin User",
                email="test_email1@example.com",
                role=UserRole.ADMIN.value,
                password_hash=get_password_hash(str(123)),
            )
            User.create(
                name="Regular User",
                email="test_email12@example.com",
                role=UserRole.WORKER.value,
                password_hash=get_password_hash(str(123)),
            )
    return db


database = db_init()
