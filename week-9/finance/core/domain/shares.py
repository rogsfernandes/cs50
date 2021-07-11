from core.domain.stock import Stock


class Share:
    stock: Stock
    number: int
    total: float

    def __init__(self, stock: Stock, number: int):
        self.stock = stock
        self.number = number
        self.total = float(stock.price * number)
