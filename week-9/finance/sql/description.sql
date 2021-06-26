CREATE TABLE users (
id INTEGER PRIMARY KEY,
username TEXT NOT NULL,
hash TEXT NOT NULL,
cash NUMERIC NOT NULL DEFAULT 10000.00
);
CREATE UNIQUE INDEX username ON users (username);

CREATE TABLE stocks (
id INTEGER PRIMARY KEY,
name TEXT NOT NULL,
symbol TEXT NOT NULL
);
CREATE INDEX stock_symbol ON stocks (symbol);

CREATE TABLE transactions (
id INTEGER PRIMARY KEY,
user_id INTEGER NOT NULL REFERENCES users(id),
stock_id INTEGER NOT NULL REFERENCES stocks(id),
quantity NUMERIC NOT NULL,
price NUMERIC NOT NULL,
total NUMERIC NOT NULL,
type TEXT NOT NULL
);

CREATE INDEX user_id ON transactions (user_id);
CREATE INDEX stock_id ON transactions (stock_id);
CREATE INDEX transaction_type ON transactions (type);