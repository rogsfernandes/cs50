from server.database.sqlite import db


class PortfolioService:
    def get(self, user):
        rows = db.execute(
            "SELECT symbol, AVG(price),SUM(total), SUM(quantity) FROM transactions GROUP BY symbol HAVING user_id = ?;",
            user.id)
