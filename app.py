from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

@app.route('/')
def login():
    return render_template('login.html')

@app.route('/perform_login', methods=['POST'])
def perform_login():
    username = request.form['username']
    password = request.form['password']

    if username == "amrita" and password == "123":
        return "Login Successful!"
    else:
        return "Invalid credentials", 401

@app.route('/signup')
def signup():
    return render_template('signup.html')

@app.route('/forgot_password')
def forgot_password():
    return "Forgot password page under construction"

@app.route('/submit-signup', methods=['POST'])
def submit_signup():
    firstName = request.form['firstName']
    middleName = request.form['middleName']
    lastName = request.form['lastName']
    dob = request.form['dob']
    email = request.form['email']
    mobile = request.form['mobile']
    country = request.form['country']
    password = request.form['password']  
    confirmPassword = request.form['confirmPassword']  
    gender = request.form['gender']
    
    return "Signup successful! Welcome, {}".format(firstName)


@app.errorhandler(Exception)
def handle_exception(e):
    print(e)
    return str(e), 500

if __name__ == '__main__':
    app.run(debug=True)
