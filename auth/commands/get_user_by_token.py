from typing import Optional
from domain.models import User as DomainUser
from utils.token import get_user_id_from_token
from adapters.db.models import User


async def get_user_by_token(token: str) -> Optional[DomainUser]:
    user_id = get_user_id_from_token(token)
    try:
        user = User.get(User.id == user_id)
        return DomainUser(
            name=user.name, public_id=user.id, email=user.email, role=user.role
        )
    except User.DoesNotExist:
        return
