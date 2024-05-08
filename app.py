from flask import Flask, render_template, request, redirect, url_for
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)

    def __repr__(self):
        return f'<User {self.username}>'
    


def setup_database(app):
    with app.app_context():
        db.create_all()

setup_database(app)


    
@app.route('/')
def login():
    return render_template('login.html')

@app.route('/signup')
def signup():
    return render_template('signup.html')

@app.route('/submit-signup', methods=['POST'])
def submit_signup():
    username = request.form.get('firstName')
    password = request.form.get('password')
    email = request.form.get('email')
    if not all([username, password, email]):
        return "Missing fields", 400

    hashed_password = generate_password_hash(password, method='pbkdf2:sha256')
    
    new_user = User(username=username, password=hashed_password, email=email)
    db.session.add(new_user)
    db.session.commit()
    
    return "Signup successful! Welcome, {}".format(username)

@app.route('/perform_login', methods=['POST'])
def perform_login():
    username = request.form.get('firstName')
    password = request.form.get('password')
    if not username or not password:
        return "Missing username or password", 400
    
    user = User.query.filter_by(username=username).first()
    
    if user and check_password_hash(user.password, password):
        return "Login Successful!"
    else:
        return "Invalid credentials", 401



@app.route('/forgot_password')
def forgot_password():
    return "Forgot password page under construction"










@app.errorhandler(Exception)
def handle_exception(e):
    print(e)
    return str(e), 500

if __name__ == '__main__':
    app.run(debug=True)
