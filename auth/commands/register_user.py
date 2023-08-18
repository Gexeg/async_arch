from typing import Optional

from utils.password import get_password_hash
from domain.models import User as DomainUser
from adapters.db.models import User as DBUser
from adapters.brocker_producer import produce_event


async def register_user(
    name: str, email: str, password: str, role: str
) -> Optional[DomainUser]:
    try:
        DBUser.get(DBUser.name == name)
        return
    except DBUser.DoesNotExist:
        password_hash = get_password_hash(password)

        user: DBUser = DBUser.create(
            name=name, email=email, password_hash=password_hash, role=role
        )
        domain_user = DomainUser(
            public_id=user.id, name=user.name, email=user.email, role=user.role
        )

        await produce_event(
            {
                "event": "UserCreated",
                "data": domain_user.model_dump(),
            },
            "account_streaming",
        )

        await produce_event(
            {
                "event": "UserCreated",
                "data": domain_user.model_dump(),
            },
            "account",
        )

        return domain_user
