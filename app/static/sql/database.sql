CREATE TABLE users(
    user VARCHAR(50),
    pass VARCHAR(256),
    verify VARCHAR(40),
    email VARCHAR(50),
    verified BOOLEAN
);


ALTER TABLE users ADD COLUMN id INT AUTO_INCREMENT PRIMARY KEY;

insert into users (user, email, pass, verify)
values ('phill', 'phill@balls.com', 'uxcthis', '20d41098-19bf-450b-8e11-cf1260eaa335');
