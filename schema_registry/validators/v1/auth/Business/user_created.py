from schema_registry.validators.base_message import BaseEventMessage


class BEMessageUserCreated(BaseEventMessage):
    def get_schema_path(self):
        return "v1/auth/Business/user_created.json"
