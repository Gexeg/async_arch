from typing import Optional
from domain.models import User as DomainUser, Task as DomainTask, TaskState
from adapters.db.models import User as DBUser, Task as DBTask
from utils.logger import LOG
from adapters.broker_producer import produce_event


async def complete_task(user: DomainUser, task_id: str) -> Optional[DomainTask]:
    try:
        task = DBTask.select().join(DBUser).where(DBTask.id == task_id).get()
        if task.processing_user != user:
            LOG.info("Only task worker can complete task")
            return
        task.state = TaskState.COMPLETED
        task.save()

        domain_task = DomainTask(
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

        await produce_event(
            {
                "event": "TaskCompleted",
                "data": domain_task.model_dump(),
            },
            "task_streaming",
        )

        await produce_event(
            {
                "event": "TaskCompleted",
                "data": domain_task.model_dump(),
            },
            "task",
        )
        return domain_task
    except DBUser.DoesNotExist:
        LOG.info("Wrong task id")
        return
