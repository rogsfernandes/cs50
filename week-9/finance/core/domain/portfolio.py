from typing import List

from core.domain.stock import Stock
from core.domain.user import User


class Portfolio:
    user: User
    stocks: List[Stock]
    total: float

    def __init__(self, user: User, stocks: List[Stock], total: float):
        self.user = user
        self.stocks = stocks
        self.total = total
