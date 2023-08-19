from adapters.db.models import User
from schema_registry.validators.v1.auth.CUD.user_deleted import (
    CUDMessageUserDeletedMessage,
)


async def process_user_deleted(event_data: dict):
    schema_validator = CUDMessageUserDeletedMessage()
    if not schema_validator.validate(event_data):
        return

    user_data = event_data["event_data"]
    User.delete().where(User.public_id == user_data["public_id"]).execute()
