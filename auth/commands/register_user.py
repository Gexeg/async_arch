from db.models import User as DBUser
from utils.password import get_password_hash
from domain.models import User as DomainUser
from typing import Optional


async def register_user(name: str, email: str, password: str, role: str) -> Optional[DomainUser]:
    try:
        DBUser.get(DBUser.name == name)
        return
    except DBUser.DoesNotExist:
        password_hash = get_password_hash(password)

        user: DBUser = DBUser.create(
            name=name,
            email=email,
            password_hash=password_hash,
            role=role
        )

        return DomainUser(
            id=user.id,
            name=user.name,
            email=user.email,
            role=user.role
        )

