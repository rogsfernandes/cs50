from core.domain.stock import Stock


class Transaction:
    stock: Stock
    quantity: int
    total: float
    average_price: int
    type: str

    def __init__(self, stock, quantity, total, average_price, type):
        self.stock = stock
        self.quantity = quantity
        self.total = total
        self.average_price = average_price
        self.type = type