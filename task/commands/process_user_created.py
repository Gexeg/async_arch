from adapters.db.models import User
from utils.logger import LOG


async def process_user_created(user_data: dict):
    if (
        not user_data.get("public_id")
        or not user_data.get("name")
        or not user_data.get("email")
        or not user_data.get("role")
    ):
        LOG.error("Wrong user data %s", user_data)
        return

    User.insert(
        public_id=user_data["public_id"],
        role=user_data["role"],
        name=user_data["name"],
        email=user_data["email"],
    ).on_conflict("replace").execute()
