from core.domain.portfolio import Portfolio
from core.domain.stock import Stock
from core.domain.transaction import Transaction
from server.database.sqlite import db


class PortfolioService:
    def get(self, user):
        rows = db.execute(
            "SELECT transactions.id as id, stocks.name as name, stocks.symbol as symbol, AVG(price) as average_price, SUM(total) as total, SUM(quantity) as quantity FROM transactions JOIN users on users.id = transactions.user_id JOIN stocks on stocks.id = transactions.stock_id GROUP BY symbol HAVING user_id = ?;",
            user.id)

        portfolio = Portfolio(user,
                              [Transaction(Stock(None, row["name"], row["symbol"], None),
                                           row["quantity"],
                                           row["total"],
                                           row["average_price"]) for row in rows])

        return portfolio
