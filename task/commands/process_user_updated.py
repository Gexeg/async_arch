from adapters.db.models import User
from utils.logger import LOG


async def process_user_updated(user_data: dict):
    if (
        not user_data.get("public_id")
        or not user_data.get("name")
        or not user_data.get("email")
        or not user_data.get("role")
    ):
        LOG.error("Wrong user data %s", user_data)
        return

    User.update(
        role=user_data["role"],
    ).where(User.public_id == user_data["public_id"]).execute()
