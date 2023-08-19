from schema_registry.validators.base_message import BaseEventMessage


class CUDMessageTaskUpdated(BaseEventMessage):
    def get_schema_path(self):
        return "v1/task/CUD/task_updated.json"
