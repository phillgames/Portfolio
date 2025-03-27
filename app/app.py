
from flask import Flask, request, render_template, redirect, url_for, flash, jsonify, session #type: ignore
from flask_login import LoginManager, login_user, login_required, logout_user, current_user #type: ignore
from flask_mail import Mail, Message #type: ignore
from modules import User, get_db_connection, bcrypt
from my_secret import SECRET_KEY
import uuid
import socket

from flask import Flask, request, jsonify, render_template, redirect, url_for, flash, session # type: ignore


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
app.config['MAIL_PASSWORD'] = 'hbwj lnbx yeqh rife'

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
@login_required
def home():
    return render_template('home.html')

@app.route('/submit')
def submit():
    return render_template('home.html')

@app.route('/account')
def account():
    return render_template('account.html')

@app.route('/ourforms')
@login_required
def ourforms():
    return render_template('ourform.html')

@app.route('/results')
@login_required
def results():
    return render_template('results.html')

@app.route('/aboutme')
def aboutme():
    return render_template('aboutme.html')



@app.route('/signin', methods=['GET', 'POST'])
def signin():
    if request.method == 'POST':
        email = request.form['email']  
        password = request.form['password']
        user = User.get_user_by_email(email)  

        if user and bcrypt.check_password_hash(user.password, password):
            login_user(user)
            return redirect(url_for('aboutme'))
        else:
            flash('Invalid email or password', 'danger')

    return render_template('login.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        email = request.form.get('email')  # Changed to 'email'
        password = request.form.get('password')
        if User.get_user_by_email(email):  # Changed to 'get_user_by_email'
            flash('Email already taken', 'warning')
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
@login_required
def form():
    if request.method == 'POST':
        experience = request.form.get('experience')
        reuse = request.form.get('reuse')
        better = request.form.get('better')
        print(experience, reuse, better)
        if not experience and not reuse and not better:  # Check if all inputs are empty
            flash('You need an input to submit')
            return redirect(url_for('form'))
        else:
            User.register_input_experience(experience, reuse, better)
            return redirect(url_for('results'))  # Redirect to home after submission
    
    return render_template('ourform.html')

@app.route('/api/form-data')
def get_form_data():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT experience, reuse, better, COUNT(*) as count FROM formanswer GROUP BY experience, reuse, better")
    data = cur.fetchall()
    conn.close()

    form_data = [{'experience': row['experience'], 'reuse': row['reuse'], 'better': row['better'], 'count': row['count']} for row in data]

    return jsonify(form_data)



@app.route('/logout', methods=['POST'])
@login_required
def logout():
    logout_user()
    flash("You have been logged out.", "success")
    return redirect(url_for('account'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=4500, debug=True)
