import uuid
import datetime
from random import choice
from domain.models import User as DomainUser, Task as DomainTask, TaskState, UserRole
from adapters.db.models import User as DBUser, Task as DBTask
from utils.log_singleton import LOG
from adapters.broker_producer import produce_event
from adapters.db.db_init import database
from schema_registry.validators.v1.task.CUD.task_updated import CUDMessageTaskUpdated
from schema_registry.validators.v1.task.Business.task_asigned import (
    BEMessageTaskAssigned,
)


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

        task_assigned_message = {
            "event_id": str(uuid.uuid4()),
            "event_version": 1,
            "event_name": "TaskAssigned",
            "event_type": "Business",
            "producer": "task_service",
            "event_time": datetime.datetime.now().isoformat(),
            "event_data": domain_task.model_dump(),
        }
        task_assigned_message_validator = BEMessageTaskAssigned()
        if task_assigned_message_validator.validate(task_assigned_message):
            await produce_event(
                task_assigned_message,
                "task",
            )
