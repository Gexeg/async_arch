from random import randint
from adapters.db.models import Task, User
from schema_registry.validators.v1.task.CUD.task_created import (
    CUDMessageTaskCreated as v1TaskValidator,
)
from schema_registry.validators.v2.task.CUD.task_created import (
    CUDMessageTaskCreated as v2TaskValidator,
)


async def process_task_created(event_data: dict):
    if not v1TaskValidator().validate(event_data) and not v2TaskValidator().validate(
        event_data
    ):
        return
    task_data = event_data["event_data"]

    user = User.get(User.public_id == task_data["processing_user"]["public_id"])

    Task.insert(
        public_id=task_data["public_id"],
        title=task_data.get("title"),
        description=task_data["description"],
        state=task_data["state"],
        assign_cost=randint(-20, -10),
        reward=randint(20, 40),
        processing_user=user.id,
    ).on_conflict("replace").execute()
