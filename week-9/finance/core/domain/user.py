from functools import reduce
from typing import List

from core.domain.shares import Share


class User:
    id: int
    username: str
    password: str
    cash: float
    shares: List[Share]
    total: float
    balance: float
    __hash: str

    def __init__(self, id, username, cash, hash: str, shares: List[Share]):
        self.id = id
        self.username = username
        self.cash = cash
        self.__hash = hash
        self.set_shares(shares)
        self.balance = self.cash + self.total

    def get_hash(self):
        return self.__hash

    def set_shares(self, shares):
        self.shares = shares
        self.total = reduce(lambda acc, value: acc + value.total, shares, 0)
