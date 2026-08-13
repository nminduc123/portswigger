from flask import Blueprint, request, render_template_string
import hashlib
from db import get_db_connection

# Khởi tạo blueprint cho phần đăng ký
regis_bp = Blueprint('regis', __name__)

HTML_REGISTER = '''
<!DOCTYPE html>
<html>
<head><title>SQLi Lab - Register</title></head>
<body>
    <h2>Đăng ký Tài khoản</h2>
    <form method="POST" action="/register">
        Username: <input type="text" name="username"><br><br>
        Password: <input type="password" name="password"><br><br>
        <input type="submit" value="Register">
    </form>
</body>
</html>
'''

@regis_bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template_string(HTML_REGISTER)
        
    username = request.form.get('username', '')
    password = request.form.get('password', '')
    
    pwd_hash = hashlib.sha256(password.encode()).hexdigest()
    
    conn = get_db_connection()
    cursor = conn.cursor()
    
    query = "INSERT INTO users (username, password_hash) VALUES (%s, %s)"
    cursor.execute(query, (username, pwd_hash))
    conn.commit()
    
    conn.close()
    return "Đăng ký thành công! <a href='/login'>Quay lại Đăng nhập</a>"