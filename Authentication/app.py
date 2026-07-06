from flask import Flask, request, make_response, render_template_string, redirect
import random

app = Flask(__name__)

# Cấu hình Database giả lập
USERS = {"wiener": "peter", "carlos": "montoya"}
MFA_DATABASE = {} # Nơi lưu mã MFA sinh ra cho từng user

# Giao diện HTML siêu đơn giản
HTML_LOGIN = """
    <h2>Đăng nhập (Bước 1)</h2>
    <form method="POST">
        Username: <input type="text" name="username"><br><br>
        Password: <input type="password" name="password"><br><br>
        <button type="submit">Login</button>
    </form>
"""

HTML_MFA = """
    <h2>Xác thực 2FA (Bước 2)</h2>
    <p>Đang yêu cầu mã cho tài khoản: <b>{{ user }}</b></p>
    <form method="POST">
        Mã MFA (4 số): <input type="text" name="mfa-code"><br><br>
        <button type="submit">Xác nhận</button>
    </form>
"""

# ==========================================
# LUỒNG LOGIC CỦA TRANG WEB
# ==========================================

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return HTML_LOGIN
    
    # Xử lý khi user bấm nút Login
    user = request.form.get('username')
    pwd = request.form.get('password')
    
    if USERS.get(user) == pwd:
        # [LỖ HỔNG LÀ Ở ĐÂY - SAI LẦM 1]
        # Đáng lẽ phải lưu user vào Session an toàn trên Server, 
        # lập trình viên lại ném thẳng tên user vào Cookie gửi về cho Client.
        resp = make_response(redirect('/login2'))
        resp.set_cookie('verify', user) 
        return resp
    return "Sai username hoặc password!"

@app.route('/login2', methods=['GET', 'POST'])
def mfa():
    # Đọc xem Client gửi lên Cookie verify là ai
    target_user = request.cookies.get('verify')
    
    if not target_user:
        return redirect('/login')

    if request.method == 'GET':
        # [HẬU QUẢ CỦA LỖ HỔNG 1]
        # Server ngây thơ tin tưởng cái cookie. 
        # Nếu Hacker đổi cookie thành verify=carlos, hệ thống sẽ sinh mã cho carlos!
        mfa_code = f"{random.randint(0, 9999):04d}"
        MFA_DATABASE[target_user] = mfa_code 
        
        # In log ra màn hình console để bạn đóng vai "Email của hệ thống"
        print(f"\n[HỆ THỐNG] Đã gửi mã bí mật {mfa_code} tới email của: {target_user}\n")
        
        return render_template_string(HTML_MFA, user=target_user)

    if request.method == 'POST':
        user_input_code = request.form.get('mfa-code')
        real_code = MFA_DATABASE.get(target_user)
        
        # [LỖ HỔNG LÀ Ở ĐÂY - SAI LẦM 2]
        # Không hề có biến đếm số lần nhập sai. Nhập sai thì báo lỗi rồi cho nhập tiếp vô hạn.
        if user_input_code == real_code:
            resp = make_response(f"<h1>CHÚC MỪNG! BẠN ĐÃ ĐĂNG NHẬP THÀNH CÔNG VÀO TÀI KHOẢN: {target_user.upper()}</h1>")
            resp.set_cookie('session', f"SUPER_SECRET_SESSION_OF_{target_user}")
            return resp
        else:
            return "Sai mã MFA rồi! Vui lòng back lại và thử lại.", 200

if __name__ == '__main__':
    app.run(port=5000, debug=True)