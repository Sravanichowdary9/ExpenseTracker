from flask import Flask, render_template, request, redirect, url_for
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

@app.route('/')
def login():
    return render_template('login.html')

@app.route('/perform_login', methods=['POST'])
def perform_login():
    username = request.form['username']
    password = request.form['password']
    
    user = User.query.filter_by(username=username).first()
    
    if user and check_password_hash(user.password, password):
        return "Login Successful!"
    else:
        return "Invalid credentials", 401


@app.route('/signup')
def signup():
    return render_template('signup.html')

@app.route('/forgot_password')
def forgot_password():
    return "Forgot password page under construction"



class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)

    def __repr__(self):
        return f'<User {self.username}>'

@app.before_first_request
def create_tables():
    db.create_all()


@app.route('/submit-signup', methods=['POST'])
def submit_signup():
    username = request.form['username']
    password = request.form['password']
    email = request.form['email']
    
    hashed_password = generate_password_hash(password, method='sha256')
    
    new_user = User(username=username, password=hashed_password, email=email)
    db.session.add(new_user)
    db.session.commit()
    
    return "Signup successful! Welcome, {}".format(username)


@app.errorhandler(Exception)
def handle_exception(e):
    print(e)
    return str(e), 500

if __name__ == '__main__':
    app.run(debug=True)
