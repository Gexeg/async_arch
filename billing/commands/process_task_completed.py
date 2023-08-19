from adapters.db.models import Task, User, Transaction, TransactionType
from schema_registry.validators.v1.task.Business.task_completed import (
    BEMessageTaskCompleted,
)


async def process_task_completed(event_data: dict):
    schema_validator = BEMessageTaskCompleted()
    if not schema_validator.validate(event_data):
        return
    task_data = event_data["event_data"]

    user = User.get(User.public_id == task_data["processing_user"]["public_id"])
    task = Task.get(Task.public_id == task_data["public_id"])
    Transaction.insert(
        user_id=user.id,
        transaction_type=TransactionType.task_completed,
        amount=task.reward,
        data={"task_id": task.id},
    ).execute()
