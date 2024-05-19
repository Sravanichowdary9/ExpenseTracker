from flask import Flask, render_template, redirect, url_for, request, flash
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, TelField, DateField, FloatField, SelectField
from wtforms.validators import InputRequired, Email, Length, Optional, EqualTo
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
import email_validator  # Ensures valid email addresses
from datetime import datetime

app = Flask(__name__)
app.config['SECRET_KEY'] = 'ExpenseTracker'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///../database.db'
Bootstrap(app)
db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

# Models

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(30), unique=True, nullable=False)
    password = db.Column(db.String(80), nullable=False)
    firstName = db.Column(db.String(20), nullable=False)
    lastName = db.Column(db.String(20), nullable=False)
    city = db.Column(db.String(100), nullable=False)
    expenses = db.relationship('Expense', backref='user', lazy=True)

class Expense(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    category = db.Column(db.String(50))
    month = db.Column(db.Integer)
    year = db.Column(db.Integer)
    amount = db.Column(db.Float)

# Forms

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[InputRequired(), Length(min=4, max=20)])
    password = PasswordField('Password', validators=[InputRequired(), Length(min=5, max=80)])
    remember = BooleanField('Remember me')

class RegisterForm(FlaskForm):
    email = StringField('Email', validators=[InputRequired(), Email(message="Invalid Email"), Length(min=6, max=30)])
    username = StringField('Username', validators=[InputRequired(), Length(min=4, max=20)])
    password = PasswordField('Password', validators=[InputRequired(), Length(min=5, max=80)])
    confirmPassword = PasswordField('Confirm Password', validators=[InputRequired(), EqualTo('password', message="Passwords must match")])
    firstName = StringField('First Name', validators=[InputRequired(), Length(min=1, max=30)])
    middleName = StringField('Middle Name', validators=[Optional(), Length(max=30)])  
    lastName = StringField('Last Name', validators=[InputRequired(), Length(min=1, max=30)])
    dob = DateField('Date of Birth', format='%Y-%m-%d', validators=[InputRequired()])
    mobile = TelField('Mobile', validators=[InputRequired(), Length(min=6, max=15)])
    city = StringField('City', validators=[InputRequired(), Length(min=2)])

class ExpenseForm(FlaskForm):
    category = SelectField('Category', choices=[('Rent', 'Rent'), ('Transportation', 'Transportation'), ('Utilities', 'Utilities'), ('Groceries', 'Groceries'), ('Eating Out', 'Eating Out'), ('Other', 'Other')], validators=[InputRequired()])
    amount = FloatField('Amount', validators=[InputRequired()])
    date = DateField('Date', format='%Y-%m-%d', validators=[InputRequired()])

# Routes

@app.route('/')
def home():
    return render_template('landing.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            return redirect(url_for('dashboard'))
        flash('Invalid username or password', 'error')
    return render_template('login.html', form=form)

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    form = RegisterForm()
    if form.validate_on_submit():
        hashed_password = generate_password_hash(form.password.data, method='pbkdf2:sha256')
        new_user = User(username=form.username.data,
                        email=form.email.data,
                        password=hashed_password,
                        firstName=form.firstName.data,
                        lastName=form.lastName.data,
                        city=form.city.data)
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for('login'))
    return render_template('signup.html', form=form)

@app.route('/dashboard', methods=['GET', 'POST'])
@login_required
def dashboard():
    categories = ['Rent', 'Transportation', 'Utilities', 'Groceries', 'Eating Out', 'Other']
    expenses = Expense.query.filter_by(user_id=current_user.id).all()
    form = ExpenseForm()
    if form.validate_on_submit():
        new_expense = Expense(user_id=current_user.id, category=form.category.data, amount=form.amount.data, date=form.date.data)
        db.session.add(new_expense)
        db.session.commit()
        return redirect(url_for('dashboard'))
    return render_template('dashboard.html', name=current_user.username, categories=categories, expenses=expenses, form=form)

@app.route('/submit_expense', methods=['POST'])
@login_required
def submit_expense():
    form = ExpenseForm()
    if form.validate_on_submit():
        category = form.category.data
        amount = form.amount.data
        date = form.date.data
        month = date.month
        year = date.year
        new_expense = Expense(user_id=current_user.id, category=category, amount=amount, month=month, year=year)
        db.session.add(new_expense)
        db.session.commit()
        return redirect(url_for('dashboard'))
    return 'Failed to submit expense', 400


@app.route('/create_group', methods=['POST'])
@login_required
def create_group():
    # Implement group creation logic here
    return 'http://generated.group.url'

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('home'))

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=9000, debug=True, threaded=True)
