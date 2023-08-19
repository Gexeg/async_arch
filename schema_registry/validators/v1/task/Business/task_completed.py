from schema_registry.validators.base_message import BaseEventMessage


class BEMessageTaskCompleted(BaseEventMessage):
    def get_schema_path(self):
        return "v1/task/Business/task_completed.json"
