import datetime
from adapters.db.models import User, Transaction, UserAccount


async def get_my_account(user_public_id: str):
    today = datetime.datetime.combine(
        datetime.date.today(), datetime.datetime.min.time()
    )
    try:
        user = User.get(User.public_id == user_public_id)
    except Exception:
        return
    try:
        account = UserAccount.get(
            UserAccount.user_id == user.id, UserAccount.created == today
        )
        return {"user": user_public_id, "amount": account.amount, "date": today}
    except Exception:
        return
