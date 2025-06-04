CREATE DATABASE portfoliousr;

CREATE TABLE users(
    email VARCHAR(50),
    password VARCHAR(256),
    id INT AUTO_INCREMENT PRIMARY KEY
);


CREATE TABLE coms(
    userid INT,
    Comments VARCHAR(256),
    id INT AUTO_INCREMENT PRIMARY KEY
);


insert into users (email, password)
values ('test@email.com', 'youshouldnotseethis');
