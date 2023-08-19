from adapters.db.models import User
from schema_registry.validators.v1.auth.CUD.user_updated import CUDMessageUserUpdated


async def process_user_updated(event_data: dict):
    schema_validator = CUDMessageUserUpdated()
    if not schema_validator.validate(event_data):
        return

    user_data = event_data["event_data"]
    User.update(
        role=user_data["role"],
    ).where(User.public_id == user_data["public_id"]).execute()
