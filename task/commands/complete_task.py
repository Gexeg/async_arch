from typing import Optional
from random import choice
from domain.models import User as DomainUser, Task as DomainTask, UserRole
from adapters.db.models import User as DBUser, Task as DBTask
from utils.logger import LOG


async def create_new_task(
    user: DomainUser, task_description: str
) -> Optional[DomainTask]:
    if user.role == UserRole.WORKER:
        LOG.warning("worker can't create tasks")
        return

    workers = [
        worker for worker in DBUser.select().where(DBUser.role == UserRole.WORKER)
    ]
    if not workers:
        LOG.warning("Could not find workers to assign to the task")
        return

    chosen_one: DBUser = choice(workers)
    new_task = DBTask.create(
        description=task_description, processing_user=chosen_one.id
    )
    return DomainTask(
        description=new_task.description,
        public_id=new_task.id,
        state=new_task.state,
        processing_user=DomainUser(
            public_id=chosen_one.public_id,
            name=chosen_one.name,
            email=chosen_one.email,
            role=chosen_one.role,
        ),
    )
