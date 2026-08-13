from flask import Blueprint, request, session, render_template_string, redirect, current_app, jsonify
import hashlib
import os
from db import get_db_connection

# Khởi tạo blueprint cho phần login
login_bp = Blueprint('login', __name__)

HTML_LOGIN = '''
<!DOCTYPE html>
<html>
<head><title>SQLi Lab - Login</title></head>
<body>
    <h2>Đăng nhập</h2>
    <form method="POST" action="/login">
        Username: <input type="text" name="username"><br><br>
        Password: <input type="password" name="password"><br><br>
        <input type="submit" value="Login">
    </form>
</body>
</html>
'''

@login_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template_string(HTML_LOGIN)
        
    username = request.form.get('username', '')
    password = request.form.get('password', '')
    
    pwd_hash = hashlib.sha256(password.encode()).hexdigest()
    
    conn = get_db_connection()
    cursor = conn.cursor()

    # VULNERABLE CODE: Lỗi SQL Injection
    query = f"SELECT id, username FROM users WHERE username = '{username}' AND password_hash = '{pwd_hash}'"
    
    cursor.execute(query)
    user = cursor.fetchone()
    conn.close()

    if user:
        auth_mode = current_app.config.get('AUTH_MODE')
        
        if auth_mode == 'session':
            session['user'] = user[1]
            return redirect('/')
            
        elif auth_mode == 'token':
            # Cấp phát token ngẫu nhiên
            token = hashlib.sha256(os.urandom(24)).hexdigest()
            return jsonify({
                "status": "success",
                "username": user[1],
                "token": token,
                "message": f"Truy cập trang chủ bằng cách thêm /?token={token} vào URL"
            })
    else:
        return "Sai thông tin đăng nhập! <a href='/login'>Thử lại</a>"

@login_bp.route('/logout')
def logout():
    session.pop('user', None)
    return redirect('/')