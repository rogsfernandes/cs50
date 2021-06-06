class Stock:
    name: str
    symbol: str
    price: float

    def __init__(self, name, symbol, price):
        self.name = name
        self.symbol = symbol
        self.price = price