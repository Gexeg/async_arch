from db.models import User
from utils.password import verify_password
from utils.token import create_access_token


async def create_token(username: str, password: str):
    try:
        user = User.get(User.name==username)
    except User.DoesNotExist:
        return

    if not verify_password(password, user.password_hash):
        return

    return create_access_token(user.id)

