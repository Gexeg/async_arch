from enum import Enum
from pydantic import BaseModel


class UserRole(str, Enum):
    ADMIN = "admin"
    MANAGER = "manager"
    WORKER = "worker"


class User(BaseModel):
    public_id: int
    email: str
    role: UserRole
    name: str


class TaskState(str, Enum):
    PROCESSING = "PROCESSING"
    COMPLETED = "COMPLETED"


class Task(BaseModel):
    public_id: int
    title: str
    description: str
    state: TaskState
    processing_user: User
