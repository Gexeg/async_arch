from adapters.db.models import User as DBUser
import uuid
import datetime
from adapters.brocker_producer import produce_event
from schema_registry.validators.v1.auth.CUD.user_deleted import (
    CUDMessageUserDeletedMessage,
)

# from utils.logger import LOG


async def delete_user(public_id: str) -> None:
    try:
        DBUser.delete().where(DBUser.id == id).execute()
        message = {
            "event": "UserDeleted",
            "data": {"public_id": public_id},
        }

        cud_message = {
            "event_id": str(uuid.uuid4()),
            "event_version": 1,
            "event_name": "UserDeleted",
            "event_type": "CUD",
            "producer": "auth_service",
            "event_time": datetime.datetime.now().isoformat(),
            "event_data": {"public_id": public_id},
        }
        cud_message_validator = CUDMessageUserDeletedMessage()
        if cud_message_validator.validate(cud_message):
            await produce_event(
                cud_message,
                "account_streaming",
            )

    except DBUser.DoesNotExist:
        return
