from typing import Optional
from datetime import timedelta, datetime
from jose import JWTError, jwt
from settings import settings


def create_access_token(user_id: int) -> str:
    access_token_expires = (
        datetime.utcnow() + timedelta(minutes=settings.jwt_expiration_time)
    ).isoformat()
    to_encode = {"user_id": user_id, "expire": access_token_expires}
    encoded_jwt = jwt.encode(
        to_encode, settings.jwt_secret, algorithm=settings.jwt_algorithm
    )
    return encoded_jwt


def get_user_id_from_token(token) -> Optional[str]:
    try:
        payload = jwt.decode(
            token, settings.jwt_secret, algorithms=[settings.jwt_algorithm]
        )
        user_id: str = payload.get("user_id")
        return user_id
    except JWTError:
        return
