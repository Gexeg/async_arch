from schema_registry.validators.base_message import BaseEventMessage


class BEMessageUserRoleUpdated(BaseEventMessage):
    def get_schema_path(self):
        return "v1/auth/Business/user_role_updated.json"
