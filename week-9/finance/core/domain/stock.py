class Stock:
    id: int
    name: str
    symbol: str
    price: float

    def __init__(self, id, name, symbol, price):
        self.id = id
        self.name = name
        self.symbol = symbol
        self.price = price