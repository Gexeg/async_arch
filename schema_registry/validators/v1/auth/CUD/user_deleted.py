from schema_registry.validators.base_message import BaseEventMessage


class CUDMessageUserDeletedMessage(BaseEventMessage):
    def get_schema_path(self):
        return "v1/auth/CUD/user_deleted.json"
