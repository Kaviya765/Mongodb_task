from flask import Flask, request, render_template_string, redirect, url_for, session
from pymongo import MongoClient
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = 'your_secret_key'  

client = MongoClient('mongodb://localhost:27017')
db = client.contactDB
users_collection = db.users

signup_page = '''
  <h2>Signup</h2>
  <form method="POST">
    Username: <input name="username" required><br>
    Password: <input name="password" type="password" required><br>
    <button type="submit">Sign Up</button>
  </form>
  <a href="/login">Already have an account? Login here</a>
'''

login_page = '''
  <h2>Login</h2>
  <form method="POST">
    Username: <input name="username" required><br>
    Password: <input name="password" type="password" required><br>
    <button type="submit">Login</button>
  </form>
  <a href="/signup">Don't have an account? Sign up here</a>
  <p style="color:red;">{{error}}</p>
'''

home_page = '''
  <h2>Welcome {{username}}!</h2>
  <a href="/logout">Logout</a>
'''

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        if users_collection.find_one({'username': username}):
            return "User already exists. Please choose a different username."

        hashed_password = generate_password_hash(password)
        users_collection.insert_one({'username': username, 'password': hashed_password})
        return redirect(url_for('login'))

    return render_template_string(signup_page)

@app.route('/login', methods=['GET', 'POST'])
def login():
    error = ''
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        user = users_collection.find_one({'username': username})
        if user and check_password_hash(user['password'], password):
            session['username'] = username
            return redirect(url_for('home'))
        else:
            error = 'Invalid username or password'

    return render_template_string(login_page, error=error)

@app.route('/home')
def home():
    if 'username' in session:
        return render_template_string(home_page, username=session['username'])
    return redirect(url_for('login'))

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)
