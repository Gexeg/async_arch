import httpx

from domain.models import User
from typing import Optional
from settings import settings
from utils.logger import LOG


class AuthService:
    def __init__(self):
        self.base_url = (
            f"http://{settings.auth_service_host}:{settings.auth_service_port}"
        )

    async def get_user_by_token(self, token: str) -> Optional[User]:
        async with httpx.AsyncClient() as client:
            headers = {"Authorization": f"Bearer {token}"}
            response = await client.get(f"{self.base_url}/get_user", headers=headers)
            if response.status_code != 200:
                return

            try:
                user_data = response.json()
                return User(
                    public_id=user_data.get("public_id"),
                    email=user_data.get("email"),
                    role=user_data.get("role"),
                    name=user_data.get("name"),
                )
            except Exception as e:
                LOG.exception(e)
                return
