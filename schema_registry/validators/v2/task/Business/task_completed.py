from schema_registry.validators.base_message import BaseEventMessage


class BEMessageTaskCompleted(BaseEventMessage):
    def get_schema_path(self):
        return "v2/task/Business/task_completed.json"
