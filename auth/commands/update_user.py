from adapters.db.models import User as DBUser
from domain.models import User as DomainUser
from typing import Optional
from adapters.brocker_producer import produce_event


async def update_user_role(public_id: str, role: str) -> Optional[DomainUser]:
    try:
        user: DBUser = DBUser.get(DBUser.id == public_id)
        if role != user.role:
            user.role = role
            user.save()

        await produce_event(
            {
                "event": "UserRoleUpdated",
                "data": {"public_id": user.id, "role": role},
            },
            "account_streaming",
        )

        return DomainUser(
            public_id=user.id, name=user.name, email=user.email, role=user.role
        )
    except DBUser.DoesNotExist:
        return
