from flask import Flask, request, render_template
import time
import database

app = Flask(__name__)

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@app.route('/login', methods=['POST'])
def process_login():
    username = request.form.get('username')
    password = request.form.get('password')

    user_record = database.get_user(username)
    
    if not user_record:
        return render_template('index.html', error="Invalid username"), 401
        
    current_time = time.time()

    if user_record["lockout_until"] > 0 and current_time > user_record["lockout_until"]:
        user_record["failed_attempts"] = 0
        user_record["lockout_until"] = 0

    if user_record["failed_attempts"] >= 3:
        return render_template('index.html', error="Too many incorrect logins. Please try again in 1 minute."), 429
        
    is_valid = database.verify_password(username, password)
    
    if is_valid:
        user_record["failed_attempts"] = 0
        user_record["lockout_until"] = 0
        return render_template('index.html', success="Login successful"), 200
    else:
        user_record["failed_attempts"] += 1
        if user_record["failed_attempts"] >= 3:
            user_record["lockout_until"] = current_time + 60 
        return render_template('index.html', error="Invalid username or password"), 401

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000, threaded=True)