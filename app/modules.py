import pymysql #type: ignore
from flask_bcrypt import Bcrypt #type: ignore
from flask_login import UserMixin #type: ignore
from my_secret import SECRET_KEY
    
bcrypt = Bcrypt()


def get_connection():
    return pymysql.connect(
        host='localhost',
        user='portusr',
        password='portpass',
        db='portfoliousr'
    )

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
        conn = get_connection()
        cur = conn.cursor(pymysql.cursors.DictCursor)
        cur.execute("SELECT * FROM users WHERE email = %s", (email,))
        users = cur.fetchone()
        conn.close()
        if users:
            return User(users['email'], users['id'], users['password'])
        #, users['id']#
        return None

    @staticmethod
    def get_user_by_id(user_id):
        conn = get_connection()
        cur = conn.cursor() 
        cur.execute("SELECT * FROM users WHERE id = %s", (user_id))
        users = cur.fetchone()
        conn.close()
        if users:
            return User(users['email'], users['password'], users['id'])
        return None

    @staticmethod
    def register_user(email, password):
        hashed = bcrypt.generate_password_hash(password).decode('utf-8')
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("INSERT INTO users (email, password) VALUES (%s, %s)", (email, hashed))
        conn.commit()
        conn.close()

    @staticmethod
    def comment_with_id(com_id):
        conn = get_connection()
        cur = conn.cursor() 
        cur.execute("SELECT * FROM users WHERE id = %s", (com_id))
        users = cur.fetchone()
        cur.execute("INSERT INTO coms (userid) VALUES" (users), (com_id))
        conn.commit()
        conn.close()

    
    # @staticmethod
    # def register_input_experience(experience, reuse, better):
    #     conn = get_connection()
    #     cur = conn.cursor()
    #     cur.execute("INSERT INTO formanswer (experience, reuse, better, user) VALUES (%s, %s, %s, %s)", (experience, reuse, better, global_email))
    #     conn.commit()
    #     conn.close()


# DB_PATH = 'db/portfolio.db'

# def init_db():
#     conn = sqlite3.connect(DB_PATH)
#     cur = conn.cursor()
#     cur.execute("""
#         CREATE TABLE IF NOT EXISTS user (
#         id INTEGER PRIMARY KEY AUTOINCREMENT,
#         email TEXT NOT NULL,
#         password TEXT NOT NULL)
#     """)
#     cur.execute("""
#         CREATE TABLE IF NOT EXISTS formanswer (
#         id INTEGER PRIMARY KEY AUTOINCREMENT,
#         experience TEXT NOT NULL,
#         reuse TEXT NOT NULL,
#         better TEXT NOT NULL,
#         user TEXT NOT NULL)
#     """)
#     conn.commit()
#     conn.close()
#     print("Database initialized successfully")

# if __name__ == "__main__":
#     init_db()