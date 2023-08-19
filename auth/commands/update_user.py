import uuid
import datetime

from adapters.db.models import User as DBUser
from domain.models import User as DomainUser
from typing import Optional
from adapters.brocker_producer import produce_event
from schema_registry.validators.v1.auth.CUD.user_updated import CUDMessageUserUpdated
from schema_registry.validators.v1.auth.Business.user_role_updated import (
    BEMessageUserRoleUpdated,
)


async def update_user_role(public_id: str, role: str) -> Optional[DomainUser]:
    try:
        user: DBUser = DBUser.get(DBUser.id == public_id)
        if role != user.role:
            user.role = role
            user.save()

        domain_user = DomainUser(
            public_id=user.id, name=user.name, email=user.email, role=user.role
        )
        cud_message = {
            "event_id": str(uuid.uuid4()),
            "event_version": 1,
            "event_name": "UserUpdated",
            "event_type": "CUD",
            "producer": "auth_service",
            "event_time": datetime.datetime.now().isoformat(),
            "event_data": domain_user.model_dump(),
        }
        cud_message_validator = CUDMessageUserUpdated()
        if cud_message_validator.validate(cud_message):
            await produce_event(
                cud_message,
                "account_streaming",
            )
        business_message = {
            "event_id": str(uuid.uuid4()),
            "event_version": 1,
            "event_name": "UserRoleUpdated",
            "event_type": "Business",
            "producer": "auth_service",
            "event_time": datetime.datetime.now().isoformat(),
            "event_data": {"public_id": user.id, "role": role},
        }
        business_message_validator = BEMessageUserRoleUpdated()
        if business_message_validator.validate(business_message):
            await produce_event(
                business_message,
                "account",
            )
        return DomainUser(
            public_id=user.id, name=user.name, email=user.email, role=user.role
        )
    except DBUser.DoesNotExist:
        return
