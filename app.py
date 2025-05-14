from flask import Flask, render_template, request, redirect, url_for, jsonify
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
        users = load_users()

        if username in users and users[username]['password'] == password:
            stats = users[username].get('stats', {})
            return render_template('game.html', username=username, stats=stats)

        return "Invalid username or password."


    return render_template('login.html')  # Display login page

@app.route('/game')
def game():
    username = request.args.get('username')
    if not username:
        return redirect(url_for('login'))  # If no username is found, redirect to login page
    
    return render_template('game.html', username=username)


@app.route('/save_stats', methods=['POST'])
def save_stats():
    data = request.json
    username = data.get('username')
    updated_stats = data.get('stats')

    users = load_users()
    if username in users:
        users[username]['stats'] = updated_stats
        with open('users.json', 'w') as f:
            json.dump(users, f, indent=4)
        return jsonify({"success": True})

    return jsonify({"success": False, "error": "User not found"}), 400


if __name__ == '__main__':
    app.run(debug=True)

