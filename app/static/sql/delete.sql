DROP TABLE users;

TRUNCATE TABLE users;

DELETE FROM users WHERE id=2;

REVOKE ALL PRIVILEGES, GRANT OPTION FROM 'portusr'@'%';