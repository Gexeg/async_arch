from typing import Optional
import uuid
import datetime

from utils.password import get_password_hash
from domain.models import User as DomainUser
from adapters.db.models import User as DBUser
from adapters.brocker_producer import produce_event
from schema_registry.validators.v1.auth.CUD.user_created import CUDMessageUserCreated
from schema_registry.validators.v1.auth.Business.user_created import (
    BEMessageUserCreated,
)


async def register_user(
    name: str, email: str, password: str, role: str
) -> Optional[DomainUser]:
    try:
        DBUser.get(DBUser.name == name)
        return
    except DBUser.DoesNotExist:
        password_hash = get_password_hash(password)

        user: DBUser = DBUser.create(
            name=name, email=email, password_hash=password_hash, role=role
        )
        domain_user = DomainUser(
            public_id=user.id, name=user.name, email=user.email, role=user.role
        )
        cud_message = {
            "event_id": str(uuid.uuid4()),
            "event_version": 1,
            "event_name": "UserCreated",
            "event_type": "CUD",
            "producer": "auth_service",
            "event_time": datetime.datetime.now().isoformat(),
            "event_data": domain_user.model_dump(),
        }
        cud_message_validator = CUDMessageUserCreated()
        if cud_message_validator.validate(cud_message):
            await produce_event(
                cud_message,
                "account_streaming",
            )

        be_message = {
            "event_id": str(uuid.uuid4()),
            "event_version": 1,
            "event_name": "UserCreated",
            "event_type": "Business",
            "producer": "auth_service",
            "event_time": datetime.datetime.now().isoformat(),
            "event_data": domain_user.model_dump(),
        }
        be_message_validator = BEMessageUserCreated()
        if be_message_validator.validate(be_message):
            await produce_event(
                be_message,
                "account",
            )

        return domain_user
