from adapters.db.models import Task, User
from schema_registry.validators.v1.task.CUD.task_updated import CUDMessageTaskUpdated


async def process_task_updated(event_data: dict):
    schema_validator = CUDMessageTaskUpdated()
    if not schema_validator.validate(event_data):
        return
    task_data = event_data["event_data"]

    user = User.get(User.public_id == task_data["processing_user"]["public_id"])
    Task.update(
        public_id=task_data["public_id"],
        description=task_data["description"],
        state=task_data["state"],
        processing_user=user.id,
    ).where(Task.public_id == task_data["public_id"]).execute()
