# Users data query
SELECT * FROM users
JOIN users_shares on users.id = users_shares.user_id
WHERE user_id = ?;
