from enum import Enum
from pydantic import BaseModel


class UserRole(str, Enum):
    ADMIN = "admin"
    WORKER = "worker"
    MANAGER = "manager"


class User(BaseModel):
    id: int
    email: str
    role: UserRole
    name: str
