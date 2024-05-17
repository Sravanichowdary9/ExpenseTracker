from flask import Flask, jsonify, render_template
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    score = db.Column(db.Integer, nullable=False)

@app.route('/')
def leaderboard():
    return render_template('leaderboard.html')

@app.route('/api/users', methods=['GET'])
def get_users():
    users = Users.query.order_by(Users.score.desc()).all()
    users_list = [{'name': user.name, 'score': user.score} for user in users]
    return jsonify(users_list)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        # Add sample data if database is empty
        if Users.query.count() == 0:
            sample_users = [
                Users(name='Alice', score=2980),
                Users(name='Bob', score=2230),
                Users(name='Catherine', score=2130),
                Users(name='Dora', score=2980),
                Users(name='Elizabeth', score=2230),
                Users(name='Fabian', score=2130)        
            ]
            db.session.bulk_save_objects(sample_users)
            db.session.commit()
    app.run(port=8001, debug=True)
