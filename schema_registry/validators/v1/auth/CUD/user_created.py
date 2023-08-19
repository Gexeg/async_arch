from schema_registry.validators.base_message import BaseEventMessage


class CUDMessageUserCreated(BaseEventMessage):
    def get_schema_path(self):
        return "v1/auth/CUD/user_created.json"
