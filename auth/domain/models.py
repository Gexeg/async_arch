from enum import Enum
from pydantic import BaseModel


class UserRole(str, Enum):
    ADMIN = "admin"
    WORKER = "worker"
    MANAGER = "manager"


class User(BaseModel):
    public_id: int
    email: str
    role: UserRole
    name: str
