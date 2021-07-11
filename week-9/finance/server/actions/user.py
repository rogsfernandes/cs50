from core.domain.user import User
from core.services.transaction_service import TransactionService
from core.services.user_service import UserService


def register_user(username, password):
    user_service = UserService()

    # Checks if username already exists
    if user_service.get_by_username(username):
        return None

    rows = user_service.register(username, password)

    if len(rows) > 0:
        return User(rows[0]["id"], rows[0]["username"], rows[0]["cash"], rows[0]["hash"], [])
    else:
        return None


def get_user(session):
    user_id = session["user_id"]
    user_service = UserService()
    user = user_service.get_by_id(user_id)
    user.set_shares(user_service.get_shares(user.id))
    return user


def get_transactions(session):
    user_id = session["user_id"]
    transaction_service = TransactionService()
    transactions = transaction_service.get_by_user(user_id)
    return transactions
