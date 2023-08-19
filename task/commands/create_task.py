from typing import Optional
from random import choice
import uuid
import datetime
from domain.models import User as DomainUser, Task as DomainTask, UserRole
from adapters.db.models import User as DBUser, Task as DBTask
from utils.log_singleton import LOG
from adapters.broker_producer import produce_event
from schema_registry.validators.v2.task.CUD.task_created import CUDMessageTaskCreated
from schema_registry.validators.v2.task.Business.task_assigned import (
    BEMessageTaskAssigned,
)

def get_task_title(description: str):
    # Тут должна быть регулярка
    return "Awesome title"


async def create_new_task(
    user: DomainUser, task_description: str, task_title: str = None
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
    if not task_title:
        task_title = get_task_title(task_description)

    chosen_one: DBUser = choice(workers)
    new_task = DBTask.create(
        title=task_title, description=task_description, processing_user=chosen_one.id
    )
    domain_task = DomainTask(
        title=new_task.title,
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
    task_created_message = {
        "event_id": str(uuid.uuid4()),
        "event_version": 1,
        "event_name": "TaskCreated",
        "event_type": "CUD",
        "producer": "task_service",
        "event_time": datetime.datetime.now().isoformat(),
        "event_data": domain_task.model_dump(),
    }
    task_created_message_validator = CUDMessageTaskCreated()
    if task_created_message_validator.validate(task_created_message):
        await produce_event(
            task_created_message,
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
    return domain_task
