import datetime
from adapters.db.models import User, Transaction, UserAccount


async def count_account(user_public_id: str):
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
        result = 0
        delta = datetime.timedelta(hours=23, minutes=59, seconds=59)
        for transaction in Transaction.select().where(
            Transaction.created >= today, Transaction.created <= (today + delta)
        ):
            result += transaction.amount
        UserAccount.insert(user_id=user.id, amount=result, created=today)
        return {"user": user_public_id, "amount": result, "date": today}
