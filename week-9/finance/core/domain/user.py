class User:
    id: int
    username: str
    password: str
    cash: float
    hash: str

    def __init__(self, id, username, cash, hash):
        self.id = id
        self.username = username
        self.cash = cash
        self.hash = hash
