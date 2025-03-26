#!/bin/bash

# Create the main project directory and a documentation folder
mkdir -p app
mkdir -p docs
touch README.md

# Initialize a Git repository for version control
git init
git branch -M main  # Set the default branch to 'main'

# Create a .gitignore file to exclude unnecessary files from version control
cat <<EOL > .gitignore
__pycache__/
app/my_secret.py
venv/
/docs/ThingsToRemember.md

EOL

# Move into the 'app' directory where the application will live
cd app

# Create a Python virtual environment to isolate project dependencies
python -m venv venv

# Activate the virtual environment (platform-specific)
if [ "$(uname)" == "Darwin" ] || [ "$(uname)" == "Linux" ]; then
    source venv/bin/activate  # For macOS/Linux
elif [ "$(expr substr $(uname -s) 1 5)" == "MINGW" ]; then
    source venv/Scripts/activate  # For Windows
fi

# Create essential subdirectories for static files (CSS, images, JS), templates, and a database
mkdir -p db static/css static/img static/js templates

# Create a basic CSS reset in the styles.css file to ensure consistent styling across browsers
cat <<EOL > static/css/styles.css
/* Reset all margins and paddings */
* {
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}
EOL

# Create an empty script.js file for future JavaScript code
touch static/js/script.js

# Create the base HTML structure in templates/base.html to be inherited by other pages
cat <<EOL > templates/base.html
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <link rel="stylesheet" href="{{ url_for('static', filename='css/styles.css') }}">
    <script src="{{ url_for('static', filename='js/script.js') }}"></script>
    {% block head %}{% endblock %}
</head>
<body>
{% block body %}{% endblock %}
</body>
</html>
EOL

cat <<EOL > templates/dashboard.html
{% extends 'base.html' %}

{% block head %}
<title> </title>
{% endblock %}

{% block body %}
<h2>Welcome, {{ current_user.get_name_from_email() }}!</h2>
<form action="{{ url_for('logout') }}" method="POST" style="display: inline;">
    <button type="submit">Logout</button>
</form>
{% endblock %}

EOL

# Create a basic home page template that extends the base HTML template (empty for now)
cat <<EOL > templates/index.html
{% extends 'base.html' %}

{% block head %}
<title> </title>
{% endblock %}

{% block body %}

{% endblock %}
EOL

# Create the signin.html content (empty for now, to be customized later)
cat <<EOL > templates/login.html
{% extends 'base.html' %}

{% block head %}
<title> </title>
{% endblock %}

{% block body %}

{% endblock %}
EOL

# Create the signup.html content (empty for now, to be customized later)
cat <<EOL > templates/register.html
{% extends 'base.html' %}

{% block head %}
<title> </title>
{% endblock %}

{% block body %}

{% endblock %}
EOL

# Create Python files in 'app' root
touch app.py my_secret.py

# Install Flask into the virtual environment
pip install flask
pip install flask_login
pip install flask_bcrypt
pip install pysqlite3 
pip install pysqlite
pip install db-sqlite3

# Write the basic Flask app setup into app.py
cat <<EOL > app.py
from flask import Flask, request, render_template, redirect, url_for, flash, session
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from modules import User, get_db_connection, bcrypt
from my_secret import SECRET_KEY

app = Flask(__name__)
app.secret_key = SECRET_KEY  # Use the secret key from my_secret.py

# Flask-Login setup
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

# Add this function to fix the error
@login_manager.user_loader
def load_user(user_id):
    return User.get_user_by_id(user_id)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/dashboard')
@login_required
def dashboard():
    return render_template('dashboard.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']  
        password = request.form['password']
        user = User.get_user_by_email(email)  

        if user and bcrypt.check_password_hash(user.password, password):
            login_user(user)
            return redirect(url_for('dashboard'))
        else:
            flash('Invalid email or password', 'danger')

    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        email = request.form.get('email')  
        password = request.form.get('password')
        if User.get_user_by_email(email): 
            flash('Email already taken', 'warning')
        else:
            User.register_user(email, password)  
            flash('Registration successful! Please log in.', 'success')
            return redirect(url_for('login'))

    return render_template('register.html')

@app.route('/logout', methods=['POST'])
@login_required
def logout():
    logout_user()
    flash("You have been logged out.", "success")
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)

EOL

cat <<EOL > my_secret.py
SECRET_KEY = "admin123"
EOL

cat <<EOL > modules.py
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
EOL

cd ..

# Confirm that the folder structure, files, and virtual environment were created successfully
echo "✅ Project setup complete! 🎉"
echo "📂 Folder structure and essential files have been created."
echo "🐍 Virtual environment is set up and Flask is installed."
echo "📝 Don't forget to update 'my_secret.py' with your secret key!"
echo "💡 Next steps:"
echo "   1️⃣ Activate the virtual environment: source app/venv/bin/activate (Linux/macOS) or source app/venv/Scripts/activate (Windows)"
echo "   2️⃣ Initialize the database: python app/modules.py"
echo "   3️⃣ Run the application: python app/app.py"
echo " Remember to run *Modules.py* before running *app.py*"
echo "🚀 Happy coding!"

