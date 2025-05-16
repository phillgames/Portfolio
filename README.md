This is the code for my portfolio.

Things you need:
  1. A machine running linux (this is based on a raspberry pi 3 (but any raspberry pi should work) running raspberry pi os)
  2. mariadb installed and running/activated. (https://opensource.com/article/20/10/mariadb-mysql-linux)
  3. git downloaded and running. (sudo apt-get update and sudo apt-get install git-all worked on my raspberry pi)
  4. python and pip installed (sudo apt install python3 and sudo apt install pip)

Setup
(code works best on linux distros because the website requires mariadb for storing info)

Mariadb:
  1. Start mariadb 
     sudo mariadb
  2. Create the database 
     CREATE DATABASE portfoliousr;
  3. Use the database
     USE portfoliousr;
  4. Create the table
    CREATE TABLE users(
    email VARCHAR(50),
    password VARCHAR(256),
    id INT AUTO_INCREMENT PRIMARY KEY
    );
  5. Test if it worked
    INSERT INTO users (email, password)
    VALUES ('test@email.com', 'youshouldnotseethis');
    and then:
    SELECT * FROM users;
    If all works you can clear the table with:
    TRUNCATE users;
  6. That should succesfully create the database.

Website: (the following lines are commands to write in your terminal)
  1. write into the terminal on your linux machine:
     git clone https://github.com/phillgames/Portfolio
  2. enter repo:
     cd Portfolio/app/
  3. make a virtual enviroment:
     python3 -m venv venv
  4. activate virtual enviroment:
     source venv/bin/activate
  5. import libraries:
     pip install flask
     pip install flask_login
     pip install flask_mail
     pip install flask_bcrypt
  6. run the project (keep in mind the database connects over localhost so the python file needs to be run from the same computer):
     python3 app.py
