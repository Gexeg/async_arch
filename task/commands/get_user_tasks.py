from typing import Optional
from domain.models import User as DomainUser, Task as DomainTask, TaskState
from adapters.db.models import User as DBUser, Task as DBTask


async def get_user_task(user: DomainUser) -> list[Optional[DomainTask]]:
    result = []
    for task in (
        DBTask.select()
        .join(DBUser)
        .where(DBUser.public_id == user.public_id, DBTask.state != TaskState.COMPLETED)
    ):
        result.append(
            DomainTask(
                description=task.description,
                public_id=task.id,
                state=task.state,
                processing_user=DomainUser(
                    public_id=task.processing_user.public_id,
                    name=task.processing_user.name,
                    email=task.processing_user.email,
                    role=task.processing_user.role,
                ),
            )
        )
    return result
