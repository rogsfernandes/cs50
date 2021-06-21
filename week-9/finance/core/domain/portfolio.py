from functools import reduce
from typing import List

from core.domain.transaction import Transaction
from core.domain.user import User


class Portfolio:
    user: User
    shares: List[Transaction]
    total: float

    def __init__(self, user: User, shares: List[Transaction]):
        self.user = user
        self.shares = shares
        self.total = reduce(lambda acc, value: acc + value.total, shares, 0)
