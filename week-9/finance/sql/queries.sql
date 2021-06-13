# Portfolio query
SELECT transactions.id as id, stocks.name as name, stocks.symbol as symbol, AVG(price) as average_price, SUM(total) as total, SUM(quantity) as quantity FROM transactions
JOIN users on users.id = transactions.user_id
JOIN stocks on stocks.id = transactions.stock_id
GROUP BY symbol
HAVING user_id = 1;