from core.domain.stock import Stock


class Transaction:
    stock: Stock
    shares: int
    total: float
    price: int
    type: str

    def __init__(self, stock, shares, total, type):
        self.stock = stock
        self.shares = shares
        self.total = total
        self.type = type
