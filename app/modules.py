import sqlite3
from flask_bcrypt import Bcrypt
from flask_login import UserMixin

bcrypt = Bcrypt()

# Database connection function
def get_db_connection():
    conn = sqlite3.connect('db/portfolio.db')  # Adjust path if needed
    conn.row_factory = sqlite3.Row  # Enables dictionary-style access
    return conn

# User model for Flask-Login
class User(UserMixin):
    def __init__(self, id, email, password):
        self.id = id
        self.email = email
        self.password = password

    def get_name_from_email(self):
        # Split the email at the '@' symbol, then split the first part by '.'
        name_part = self.email.split('@')[0]  # Get the part before '@'
        name = name_part.replace('.', ' ').title()  # Replace dots with spaces and capitalize
        return name

    @staticmethod
    def get_user_by_email(email):
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("SELECT * FROM users WHERE email = ?", (email,))
        user = cur.fetchone()
        conn.close()
        if user:
            return User(user['id'], user['email'], user['password'])
        return None

    @staticmethod
    def get_user_by_id(user_id):
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("SELECT * FROM users WHERE id = ?", (user_id,))
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
        cur.execute("INSERT INTO users (email, password) VALUES (?, ?)", (email, hashed_pw))
        conn.commit()
        conn.close()


DB_PATH = 'db/portfolio.db'

def init_db():
    """Creates the database and users table if they don't exist."""
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            email TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL
        )
    """)
    conn.commit()
    conn.close()
    print("Database initialized successfully.")


if __name__ == "__main__":
    init_db()
