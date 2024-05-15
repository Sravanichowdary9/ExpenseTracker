from flask import Flask, render_template, redirect, url_for
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SelectField, TelField, DateField
from wtforms.validators import InputRequired, Email, Length, Optional
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
import email_validator


app = Flask(__name__)
app.config['SECRET_KEY'] = 'ExpenseTracker'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///../database.db'
Bootstrap(app)
db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20))
    email = db.Column(db.String(30), unique=True)
    password = db.Column(db.String(80))
    firstName= db.Column(db.String(20))
    lastName=db.Column(db.String(20))
    city = db.Column(db.String(100))  

# Create all tables
with app.app_context():
    db.create_all()

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class LoginForm(FlaskForm):
    username = StringField('username', validators=[InputRequired(), Length(min=4, max=20)])
    password = PasswordField('password', validators=[InputRequired(), Length(min=5, max=80)])
    remember = BooleanField('remember me')


class RegisterForm(FlaskForm):
    email = StringField('Email', validators=[InputRequired(), Email(message="Invalid Email"), Length(min=6, max=30)])
    username = StringField('Username', validators=[InputRequired(), Length(min=4, max=20)])
    password = PasswordField('Password', validators=[InputRequired(), Length(min=5, max=80)])
    firstName = StringField('First Name', validators=[InputRequired(), Length(min=1, max=30)])
    middleName = StringField('Middle Name', validators=[Optional(), Length(max=30)])  
    lastName = StringField('Last Name', validators=[InputRequired(), Length(min=1, max=30)])
    confirmPassword = PasswordField('Confirm Password', validators=[InputRequired(), Length(min=5, max=80)])
    dob = DateField('Date of Birth', format='%Y-%m-%d', validators=[InputRequired()])
    mobile = TelField('Mobile', validators=[InputRequired(), Length(min=6, max=15)])
    city = StringField('City', validators=[InputRequired(), Length(min=2)])


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()

    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user:
            # compares the password hash in the db and the hash of the password typed in the form
            if check_password_hash(user.password, form.password.data):
                login_user(user, remember=form.remember.data)
                return redirect(url_for('dashboard'))
        return 'invalid username or password'

    return render_template('login.html', form=form)


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    form = RegisterForm()

    if form.validate_on_submit():
        hashed_password = generate_password_hash(form.password.data, method='pbkdf2:sha256')
        # add the user form input which is form.'field'.data into the column which is 'field'
        new_user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()
        return 'new user has been created bro!'

    return render_template('signup.html', form=form)


@app.route('/dashboard')
@login_required
def dashboard():
    return render_template('dashboard.html', name=current_user.username)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=9000, debug=True, threaded=True)