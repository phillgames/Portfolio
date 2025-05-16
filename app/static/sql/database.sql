CREATE DATABASE portfoliousr;

CREATE TABLE users(
    email VARCHAR(50),
    password VARCHAR(256),
    id INT AUTO_INCREMENT PRIMARY KEY
);



ALTER TABLE users DROP COLUMN whatever;

insert into users (email, password)
values ('test@email.com', 'youshouldnotseethis');
