from adapters.db.models import User as DBUser
from domain.models import User as DomainUser
from typing import Optional
from adapters.brocker_producer import produce_event


async def delete_user(public_id: str) -> None:
    try:
        user: DBUser = DBUser.delete().where(DBUser.id == id).execute
        await produce_event(
            {
                "event": "UserDeleted",
                "data": {"public_id": public_id},
            },
            "account_streaming",
        )
    except DBUser.DoesNotExist:
        return
