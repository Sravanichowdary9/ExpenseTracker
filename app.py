from flask import Flask, render_template, redirect, url_for, request
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SelectField, TelField, DateField, FloatField
from wtforms.validators import InputRequired, Email, Length, Optional
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
import email_validator
import uuid
from datetime import datetime

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
    username = db.Column(db.String(20), unique=True)
    email = db.Column(db.String(30), unique=True)
    password = db.Column(db.String(80))
    firstName= db.Column(db.String(20))
    lastName=db.Column(db.String(20))
    city = db.Column(db.String(100))
    activities = db.relationship('Activity', backref='user', lazy=True)

class URL(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    url = db.Column(db.String(255), nullable=False)
    unique_id = db.Column(db.String(8), nullable=False, unique=True)

    def __repr__(self):
        return f'<URL {self.id}: {self.url}>'

class Activity(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    action = db.Column(db.String(255), nullable=False)

class Expense(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    category = db.Column(db.String(50), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    timestamp = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)


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

class ExpenseForm(FlaskForm):
    category = StringField('Expense Category', validators=[InputRequired(), Length(min=1, max=50)])
    amount = FloatField('Expense Amount', validators=[InputRequired()])
    
@app.route('/submit_expense', methods=['POST'])
@login_required
def submit_expense():
    data = request.get_json()
    category = data.get('category')
    amount = data.get('amount')

    if category and amount is not None:
        # Save the individual expense
        new_expense = Expense(user_id=current_user.id, category=category, amount=amount)
        db.session.add(new_expense)

        # Update the aggregated expenses
        aggregated_expense = UserAggregatedExpenses.query.filter_by(user_id=current_user.id).first()
        if not aggregated_expense:
            aggregated_expense = UserAggregatedExpenses(user_id=current_user.id, total_amount=amount)
            db.session.add(aggregated_expense)
        else:
            aggregated_expense.total_amount += amount

        db.session.commit()
        return {'success': True}
    return {'success': False}, 400


class UserAggregatedExpenses(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    total_amount = db.Column(db.Float, nullable=False, default=0.0)


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()

    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            return redirect(url_for('dashboard'))
        return 'Invalid username or password'

    return render_template('login.html', form=form)

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    form = RegisterForm()

    if form.validate_on_submit():
        hashed_password = generate_password_hash(form.password.data, method='pbkdf2:sha256')
        new_user = User(username=form.username.data, email=form.email.data, password=hashed_password,
                        firstName=form.firstName.data,
                        lastName=form.lastName.data,
                        city=form.city.data)
        db.session.add(new_user)
        db.session.commit()
        return 'New user has been created!'

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

@app.route('/create_group', methods=['POST'])
@login_required
def create_group():
    while True:
        unique_id = str(uuid.uuid4())[:8]
        url = f'http://expenseTracer.com/{unique_id}'

        existing_url = URL.query.filter_by(unique_id=unique_id).first()
        if not existing_url:
            break

    new_url = URL(url=url, unique_id=unique_id)
    db.session.add(new_url)
    db.session.commit()

    # Log the activity
    activity = Activity(user_id=current_user.id, action='Created a new group')
    db.session.add(activity)
    db.session.commit()

    return url


if __name__ == '__main__':
    with app.app_context():
        db.create_all()

    app.run(host='0.0.0.0', port=9000, debug=True, threaded=True)
