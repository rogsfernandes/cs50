CREATE TABLE users (
id INTEGER PRIMARY KEY,
username TEXT NOT NULL,
hash TEXT NOT NULL,
cash NUMERIC NOT NULL DEFAULT 10000.00
);
CREATE UNIQUE INDEX username ON users (username);

CREATE TABLE users_shares (
user_id INTEGER NOT NULL REFERENCES users(id),
symbol TEXT NOT NULL,
shares NUMERIC NOT NULL
);

CREATE INDEX user_id_shares ON users_shares (user_id);

CREATE TABLE transactions (
id INTEGER PRIMARY KEY,
user_id INTEGER NOT NULL REFERENCES users(id),
symbol TEXT NOT NULL,
shares NUMERIC NOT NULL,
price NUMERIC NOT NULL,
total NUMERIC NOT NULL,
type TEXT NOT NULL
);

CREATE INDEX user_id_transactions ON transactions (user_id);