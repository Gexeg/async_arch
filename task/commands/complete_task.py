from typing import Optional
import uuid
import datetime

from domain.models import User as DomainUser, Task as DomainTask, TaskState
from adapters.db.models import User as DBUser, Task as DBTask
from utils.log_singleton import LOG
from adapters.broker_producer import produce_event
from schema_registry.validators.v2.task.CUD.task_updated import CUDMessageTaskUpdated
from schema_registry.validators.v2.task.Business.task_completed import (
    BEMessageTaskCompleted,
)


async def complete_task(user: DomainUser, task_id: str) -> Optional[DomainTask]:
    try:
        user = DBUser.get(DBUser.public_id == user.public_id)
        task = DBTask.select().join(DBUser).where(DBTask.id == task_id).get()
        if int(task.processing_user_id) != int(user.id):
            LOG.info("Only task worker can complete task")
            return
        task.state = TaskState.COMPLETED
        task.save()

        domain_task = DomainTask(
            title=task.title,
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

        task_updated_message = {
            "event_id": str(uuid.uuid4()),
            "event_version": 1,
            "event_name": "TaskUpdated",
            "event_type": "CUD",
            "producer": "task_service",
            "event_time": datetime.datetime.now().isoformat(),
            "event_data": domain_task.model_dump(),
        }
        task_updated_message_validator = CUDMessageTaskUpdated()
        if task_updated_message_validator.validate(task_updated_message):
            await produce_event(
                task_updated_message,
                "task_streaming",
            )

        task_completed_message = {
            "event_id": str(uuid.uuid4()),
            "event_version": 1,
            "event_name": "TaskCompleted",
            "event_type": "Business",
            "producer": "task_service",
            "event_time": datetime.datetime.now().isoformat(),
            "event_data": domain_task.model_dump(),
        }
        task_completed_message_validator = BEMessageTaskCompleted()
        if task_completed_message_validator.validate(task_completed_message):
            await produce_event(
                task_completed_message,
                "task",
            )
        return domain_task
    except DBUser.DoesNotExist:
        LOG.info("Wrong task id")
        return
