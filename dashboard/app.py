from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
import uuid

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///urls.db'  # Change this to your database URI
db = SQLAlchemy(app)

class URL(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    url = db.Column(db.String(255), nullable=False, unique=True)

    def _repr_(self):
        return f'<URL {self.id}: {self.url}>'
'''If the page is just refreshing when you press the "Create Group" button, it's likely because the form is submitting a POST request
 but not preventing the default behavior, which is to submit the form data and refresh the page. To prevent this default behavior, 
 you can add a JavaScript function to handle the form submission asynchronously using AJAX. Here's how you can do it:

'''
@app.route('/')
def index():
    urls = URL.query.all()
    return render_template('index.html', urls=urls)

@app.route('/create_group', methods=['POST'])
def create_group():
    if request.method == 'POST':
        with app.app_context():
            # Clear existing URLs from the database
            URL.query.delete()

            unique_id = str(uuid.uuid4())[:8]  # Generate a random UUID and take the first 8 characters
            url = f'http://example.com/{unique_id}'  # Replace 'example.com' with your domain

            # Create a new URL object and save it to the database
            new_url = URL(url=url)
            db.session.add(new_url)
            db.session.commit()

    return redirect('/')

if __name__ == '_main_':
    with app.app_context():
        db.create_all()
    app.run(debug=True)