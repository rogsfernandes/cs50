CREATE TABLE transactions (
id INTEGER,
user_id INTEGER NOT NULL,
symbol TEXT NOT NULL,
quantity NUMERIC NOT NULL,
price NUMERIC NOT NULL,
total NUMERIC NOT NULL,
PRIMARY KEY(id)
);

CREATE INDEX user_id ON transactions (user_id);