from typing import List

from core.domain.transaction import Transaction
from core.domain.user import User


class Portfolio:
    user: User
    transactions: List[Transaction]
    total: float

    def __init__(self, user: User, transactions: List[Transaction], total: float):
        self.user = user
        self.transactions = transactions
        self.total = total
