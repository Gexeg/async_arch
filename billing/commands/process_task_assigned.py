from adapters.db.models import Task, User, Transaction, TransactionType
from schema_registry.validators.v1.task.Business.task_asigned import (
    BEMessageTaskAssigned,
)


async def process_task_assigned(event_data: dict):
    schema_validator = BEMessageTaskAssigned()
    if not schema_validator.validate(event_data):
        return
    task_data = event_data["event_data"]

    user = User.get(User.public_id == task_data["processing_user"]["public_id"])
    task = Task.get(Task.public_id == task_data["public_id"])
    Transaction.insert(
        user_id=user.id,
        transaction_type=TransactionType.task_assigned,
        amount=task.assign_cost,
        data={"task_id": task.id},
    ).execute()
