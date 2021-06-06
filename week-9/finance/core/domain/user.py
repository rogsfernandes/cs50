class User:
    id: int
    username: str
    password: str
    cash: float

    def __init__(self, id, username, cash):
        self.id = id
        self.username = username
        self.cash = cash
