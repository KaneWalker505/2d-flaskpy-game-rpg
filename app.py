from flask import Flask, render_template, request, redirect, url_for
import json

app = Flask(__name__)

# Load users from JSON file
def load_users():
    with open('users.json', 'r') as f:
        return json.load(f)

# Check if username exists in users.json and password matches
def check_login(username, password):
    users = load_users()
    return users.get(username) == password

@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        # Check if login credentials are valid
        if check_login(username, password):
            return redirect(url_for('game', username=username))  # Redirect to the game page with username
        else:
            return "Invalid username or password. Try again."

    return render_template('login.html')  # Display login page

@app.route('/game')
def game():
    username = request.args.get('username')
    if not username:
        return redirect(url_for('login'))  # If no username is found, redirect to login page
    
    return render_template('game.html', username=username)

if __name__ == '__main__':
    app.run(debug=True)

