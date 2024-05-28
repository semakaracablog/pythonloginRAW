from flask import Flask, render_template, redirect, url_for, request, session, flash
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = 'your_secret_key'

users = {}  # This will act as our simple database for demonstration purposes.

@app.route('/')
def home():
            if 'username' in session:
                return f'Logged in as {session["username"]} <br><br> <a href="/logout">Logout</a>'
            return 'You are not logged in. <a href="/login">Login</a> or <a href="/register">Register</a>'

@app.route('/login', methods=['GET', 'POST'])
def login():
            if request.method == 'POST':
                username = request.form['username']
                password = request.form['password']
                user = users.get(username)

                if user and check_password_hash(user['password'], password):
                    session['username'] = username
                    flash('Login successful!', 'success')
                    return redirect(url_for('home'))
                flash('Invalid credentials. Please try again.', 'danger')

            return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
            if request.method == 'POST':
                username = request.form['username']
                password = request.form['password']

                if username in users:
                    flash('Username already exists. Please choose another.', 'danger')
                else:
                    hashed_password = generate_password_hash(password)
                    users[username] = {'password': hashed_password}
                    flash('Registration successful! Please log in.', 'success')
                    return redirect(url_for('login'))

            return render_template('register.html')

@app.route('/logout')
def logout():
            session.pop('username', None)
            flash('You have been logged out.', 'success')
            return redirect(url_for('home'))

if __name__ == '__main__':
            app.run(debug=True)
    