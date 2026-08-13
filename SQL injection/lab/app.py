from flask import Flask, session, render_template_string, request
import os
from login import login_bp
from register import regis_bp

app = Flask(__name__)
app.secret_key = os.urandom(24)

# BẬT/TẮT CHẾ ĐỘ Ở ĐÂY: Thay đổi giữa 'session' hoặc 'token'
app.config['AUTH_MODE'] = 'session'

# Đăng ký Blueprint với app chính
app.register_blueprint(login_bp)
app.register_blueprint(regis_bp)

HTML_INDEX = '''
<!DOCTYPE html>
<html>
<head><title>SQLi Lab - Trang chủ</title></head>
<body>
    <h2>Trang chủ Hệ thống</h2>
    <a href="/login">Đăng nhập</a> | <a href="/register">Đăng ký tài khoản</a>
</body>
</html>
'''

@app.route('/')
def index():
    auth_mode = app.config.get('AUTH_MODE')
    
    # Kiểm tra theo chế độ Session
    if auth_mode == 'session' and 'user' in session:
        return f"Đăng nhập thành công (Session)! Chào mừng <b>{session['user']}</b>. <br><br><a href='/logout'>Đăng xuất</a>"
        
    # Kiểm tra theo chế độ Token (mô phỏng nhận qua URL parameter cho lab)
    elif auth_mode == 'token':
        token = request.args.get('token')
        if token:
            return f"Đăng nhập thành công! Hệ thống nhận diện token: <b>{token}</b> <br><br><a href='/logout'>Đăng xuất</a>"
            
    return render_template_string(HTML_INDEX)

if __name__ == '__main__':
    app.run(debug=True, port=3667)