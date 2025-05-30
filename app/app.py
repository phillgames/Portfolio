
from flask import Flask, request, render_template, redirect, url_for, flash, jsonify, session #type: ignore
from flask_login import LoginManager, login_user, login_required, logout_user, current_user #type: ignore
from flask_mail import Mail, Message #type: ignore
from modules import User, get_connection, bcrypt
from my_secret import SECRET_KEY
import uuid
import socket
from passlib.context import CryptContext #type: ignore

from flask import Flask, request, jsonify, render_template, redirect, url_for, flash, session # type: ignore

# def attempt_login(user.password, password):
#     if user:
#         # Convert the salt to bytes if it is an integer
#         if isinstance(user.salt, int):
#             user.salt = user.salt.to_bytes((user.salt.bit_length() + 7) // 8, byteorder='big')

#     # Check the password
#         if bcrypt.checkpw(password.encode('utf-8'), user.hashed_password):
#             login_user(user)
#             return True
#     return False


app = Flask(__name__)
app.secret_key = SECRET_KEY  

def runonstart(email):
    User.get_user_by_email(email) 

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'geir.translator.services@gmail.com'
app.config['MAIL_PASSWORD'] = 'xknd kreq ndcy iune'

mail = Mail(app)

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.connect(('8.8.8.8', 80))
IPAddr = s.getsockname()[0]
s.close()
print(IPAddr)

@login_manager.user_loader
def load_user(user_id):
    return User.get_user_by_id(user_id)

@app.route('/') 
def index():
    return render_template('start.html')

@app.route('/register')
def register():
    return render_template('register.html')

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/home')
def home():
    return render_template('home.html')

#     if session["logged_in"]:
#         return render_template('home.html')
#     else:
#         redirect("/login")

@app.route('/submit')
def submit():
    return render_template('home.html')

@app.route('/account')
def account():
    return render_template('account.html')

@app.route('/preview')
def preview():
    return render_template('preview.html')

@app.route('/projects')
def projects():
    return render_template('projects.html')


# @app.route('/signin', methods=['GET', 'POST'])
# def signin():
#     if request.method == 'POST':
#         email = request.form['email']  
#         password = request.form['password']
#         user = User.get_user_by_email(email)  
#         print(user.password, password)


@app.route('/signin', methods=['GET', 'POST'])
def signin():
    pass_alert = True
    if request.method == 'POST':
        email = request.form['email']  
        password = request.form['password']
        user = User.get_user_by_email(email)  

        if user and bcrypt.check_password_hash(user.password, password):
            print("u did it :)")
            session["logged_in"] = True
            session["current_user"] = email
            login_user(user)
            return redirect(url_for('home'))
        else:
            
            print("u didn't it :)")

    return render_template('login.html', pass_alert=pass_alert)

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        email = request.form.get('email')  # Changed to 'email'
        password = request.form.get('password')
        if User.get_user_by_email(email):  # Changed to 'get_user_by_email'
            return redirect(url_for('login'))
        else:
            User.register_user(email, password)  # Changed to 'register_user' with email
            flash('Registration successful! Please log in.', 'success')
            subject = "Welcome to Statistikkbyrå"
            body = f"Hello! Your account has been created successfully.\n\nClick this link http://{IPAddr}:4500/home\n\nto return to the website\n\n Best regards, \n\nThe Statistikkbyrå AS"


            msg = Message(subject, sender="your-email@gmail.com", recipients=[email])
            msg.body = body
            mail.send(msg)

            return redirect(url_for('login'))

    return render_template('register.html')

@app.route('/form', methods=['GET', 'POST'])



# @app.route('/api/form-data')
# def get_form_data():
#     conn = get_connection()
#     cur = conn.cursor()
#     cur.execute("SELECT experience, reuse, better, COUNT(*) as count FROM formanswer GROUP BY experience, reuse, better")
#     data = cur.fetchall()
#     conn.close()

#     form_data = [{'experience': row['experience'], 'reuse': row['reuse'], 'better': row['better'], 'count': row['count']} for row in data]

#     return jsonify(form_data)



@app.route('/logout', methods=['POST'])

def logout():
    if session["logged_in"]:
        redirect(url_for('account'))
        session["logged_in"] = False
    else:
        redirect("/login")
        flash("You have been logged out.", "success")
    return redirect(url_for('account'))


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
