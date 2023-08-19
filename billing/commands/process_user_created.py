from adapters.db.models import User
from schema_registry.validators.v1.auth.CUD.user_created import CUDMessageUserCreated


async def process_user_created(event_data: dict):
    schema_validator = CUDMessageUserCreated()
    if not schema_validator.validate(event_data):
        return
    user_data = event_data["event_data"]

    User.insert(
        public_id=user_data["public_id"],
        role=user_data["role"],
        name=user_data["name"],
        email=user_data["email"],
    ).on_conflict("replace").execute()
