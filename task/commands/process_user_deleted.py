from adapters.db.models import User
from utils.logger import LOG


async def process_user_deleted(user_data: dict):
    if not user_data.get("public_id"):
        LOG.error("Wrong user data %s", user_data)
        return

    User.delete().where(User.public_id == user_data["public_id"]).execute()
