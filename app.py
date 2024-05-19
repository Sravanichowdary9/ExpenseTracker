from flask import Flask, render_template, redirect, url_for, request
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, TelField, DateField, FloatField
from wtforms.validators import InputRequired, Email, Length, Optional
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
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

# Define the User model
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(30), unique=True, nullable=False)
    password = db.Column(db.String(80), nullable=False)
    firstName = db.Column(db.String(20))
    lastName = db.Column(db.String(20))
    city = db.Column(db.String(100))
    expenses = db.relationship('Expense', backref='user', lazy=True)
    groups = db.relationship('UserGroup', backref='user', lazy=True)

# Define the Group model
class Group(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    group_name = db.Column(db.String(50), nullable=False)
    group_link = db.Column(db.String(255), nullable=False, unique=True)
    members = db.relationship('UserGroup', backref='group', lazy=True)

# Define the UserGroup model to handle the many-to-many relationship between User and Group
class UserGroup(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    group_id = db.Column(db.Integer, db.ForeignKey('group.id'), nullable=False)

# Define the Expense model
class Expense(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    category = db.Column(db.String(50), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    timestamp = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

# Define the UserAggregatedExpenses model for leaderboard
class UserAggregatedExpenses(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    total_amount = db.Column(db.Float, nullable=False, default=0.0)

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

@app.route('/leaderboard')
def leaderboard():
    leaderboard_data = UserAggregatedExpenses.query.order_by(UserAggregatedExpenses.total_amount.desc()).all()
    # Fetch usernames corresponding to user_ids in leaderboard_data
    usernames = {user.id: user.username for user in User.query.all()}
    return render_template('leaderboard.html', leaderboard_data=leaderboard_data, usernames=usernames)

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
        group_link = f'http://expenseTracer.com/{unique_id}'

        existing_group = Group.query.filter_by(group_link=group_link).first()
        if not existing_group:
            break

    new_group = Group(group_name='Group', group_link=group_link)
    db.session.add(new_group)
    db.session.commit()

    # Link the user to the group
    user_group = UserGroup(user_id=current_user.id, group_id=new_group.id)
    db.session.add(user_group)
    db.session.commit()

    return group_link

@app.route('/join_group', methods=['POST'])
@login_required
def join_group():
    group_link = request.form.get('groupLink')

    # Check if the unique_id exists in the Group table
    existing_group = Group.query.filter_by(group_link=group_link).first()
    if existing_group:
        # Check if the user is already a member of the group
        user_group = UserGroup.query.filter_by(user_id=current_user.id, group_id=existing_group.id).first()
        if not user_group:
            # Link the user to the group
            user_group = UserGroup(user_id=current_user.id, group_id=existing_group.id)
            db.session.add(user_group)
            db.session.commit()

        return redirect(url_for('group_dashboard', group_id=existing_group.id))
    else:
        return 'Invalid group URL', 400
    
@app.route('/group_dashboard/<int:group_id>')
@login_required
def group_dashboard(group_id):
    # Query to get all users and their aggregated expenses in the group
    members = db.session.query(
        User.username, 
        db.func.sum(Expense.amount).label('total_expenses')
    ).join(Expense, User.id == Expense.user_id).join(UserGroup, User.id == UserGroup.user_id).filter(UserGroup.group_id == group_id).group_by(User.username).all()

    return render_template('leaderboard.html', members=members, group_id=group_id)


@app.context_processor
def utility_processor():
    def get_username(user_id):
        user = User.query.get(user_id)
        return user.username if user else 'Unknown'
    def get_total_amount(user_id):
        aggregated_expense = UserAggregatedExpenses.query.filter_by(user_id=user_id).first()
        return aggregated_expense.total_amount if aggregated_expense else 0.0

    return dict(get_username=get_username)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()

    app.run(host='0.0.0.0', port=9054, debug=True, threaded=True)


