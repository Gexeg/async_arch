from random import choice
from domain.models import User as DomainUser, Task as DomainTask, TaskState, UserRole
from adapters.db.models import User as DBUser, Task as DBTask
from utils.logger import LOG
from adapters.broker_producer import produce_event
from adapters.db.db_init import database


async def assign_tasks(user: DomainUser):
    if user.role not in [UserRole.ADMIN, UserRole.MANAGER]:
        LOG.info("Wtong user role to assign tasks %s", user)
        return

    events = []
    with database.atomic():
        workers = [
            worker for worker in DBUser.select().where(DBUser.role == UserRole.WORKER)
        ]
        if not workers:
            return
        for task in DBTask.select().where(DBTask.state != TaskState.COMPLETED):
            task_worker = choice(workers)
            task.processing_user = task_worker.id
            task.save()
            events.append((task_worker, task))
    for worker, task in events:
        domain_task = DomainTask(
            description=task.description,
            public_id=task.id,
            state=task.state,
            processing_user=DomainUser(
                public_id=task.public_id,
                name=task.name,
                email=task.email,
                role=task.role,
            ),
        )
        await produce_event(
            {
                "event": "TaskUpdated",
                "data": domain_task.model_dump(),
            },
            "task_streaming",
        )

        await produce_event(
            {
                "event": "TaskAssigned",
                "data": domain_task.model_dump(),
            },
            "task",
        )
