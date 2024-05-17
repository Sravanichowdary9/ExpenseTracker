from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
import uuid

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///urls.db'
db = SQLAlchemy(app)

class URL(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    url = db.Column(db.String(255), nullable=False)
    unique_id = db.Column(db.String(8), nullable=False, unique=True)


    def __repr__(self):
        return f'<URL {self.id}: {self.url}>'

@app.route('/')
def index():
    # Query the most recent URL
    recent_url = URL.query.order_by(URL.id.desc()).first()
    return render_template('index.html', recent_url=recent_url)

@app.route('/create_group', methods=['POST'])
def create_group():
    # Ensure the URL is unique
    while True:
        unique_id = str(uuid.uuid4())[:8]
        url = f'http://expenseTracer.com/{unique_id}'

        # Check if this unique_id already exists in the database
        existing_url = URL.query.filter_by(unique_id=unique_id).first()
        if not existing_url:
            break

    # Create a new URL object with the generated unique_id and save it to the database
    new_url = URL(url=url, unique_id=unique_id)
    db.session.add(new_url)
    db.session.commit()

    return url


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    
    app.run(host='0.0.0.0', port=9054, debug=True, threaded=True)