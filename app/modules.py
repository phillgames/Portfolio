import sqlite3
from flask_bcrypt import Bcrypt
from flask_login import UserMixin
from my_secret import SECRET_KEY

bcrypt = Bcrypt()


def get_db_connection():
    conn = sqlite3.connect('db/portfolio.db')
    conn.row_factory = sqlite3.Row
    return conn

class User(UserMixin):
    def __init__(self, id, email, password):
        self.id = id
        self.email = email
        self.password = password

    def get_name_from_email(self):
        name_part = self.email.split('@')[0]
        name = name_part.replace('.','.').title()
        return name

    @staticmethod
    def get_user_by_email(email):
        global global_email
        global_email = email
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("SELECT * FROM user WHERE email =?", (email,))
        user = cur.fetchone()
        conn.close()
        if user:
            return User(user['id'], user['email'], user['password'])
        return None

    @staticmethod
    def get_user_by_id(user_id):
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("SELECT * FROM user WHERE id = ?", (user_id,))
        user = cur.fetchone()
        conn.close()
        if user:
            return User(user['id'], user['email'], user['password'])
        return None

    @staticmethod
    def register_user(email, password):
        hashed_pw = bcrypt.generate_password_hash(password).decode('utf-8')
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("INSERT INTO user (email, password) VALUES (?, ?)", (email, hashed_pw))
        conn.commit()
        conn.close()
    
    @staticmethod
    def register_input_experience(experience, reuse, better):
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("INSERT INTO formanswer (experience, reuse, better, user) VALUES (?, ?, ?, ?)", (experience, reuse, better, global_email))
        conn.commit()
        conn.close()


DB_PATH = 'db/portfolio.db'

def init_db():
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS user (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        email TEXT NOT NULL,
        password TEXT NOT NULL)
    """)
    cur.execute("""
        CREATE TABLE IF NOT EXISTS formanswer (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        experience TEXT NOT NULL,
        reuse TEXT NOT NULL,
        better TEXT NOT NULL,
        user TEXT NOT NULL)
    """)
    conn.commit()
    conn.close()
    print("Database initialized successfully")

if __name__ == "__main__":
    init_db()