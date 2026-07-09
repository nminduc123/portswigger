from flask import Flask, request

app = Flask(__name__)

# Mô phỏng Database lưu trữ người dùng
DATABASE = {
    "carlos": {
        "password": "carlos_old_password",
        "reset_token": "token_carlos_999"
    },
    "wiener": {
        "password": "wiener_old_password",
        "reset_token": "token_wiener_123" # Token hợp lệ của wiener
    }
}

@app.route('/forgot-password', methods=['POST'])
def reset_password():
    # Nhận các tham số từ Request do trình duyệt (hoặc Burp Suite) gửi lên
    token = request.form.get('temp-forgot-password-token')
    username = request.form.get('username')
    new_password = request.form.get('new_password')

    # BƯỚC 1: Kiểm tra xem Token có tồn tại trong hệ thống hay không
    is_valid_token = False
    for user, data in DATABASE.items():
        if data["reset_token"] == token:
            is_valid_token = True
            break
            
    # BƯỚC 2: Xử lý cập nhật mật khẩu (Chứa LỖI LOGIC)
    if is_valid_token:
        # HỆ QUẢ LỖI: Chỉ cần token hợp lệ (của bất kỳ ai), 
        # Server sẽ mù quáng cập nhật mật khẩu cho cái tên nằm trong biến 'username'.
        if username in DATABASE:
            DATABASE[username]["password"] = new_password
            return f"Thành công! Đã đổi mật khẩu cho tài khoản: {username}", 200
        else:
            return "Lỗi: Username không tồn tại", 404
    else:
        return "Lỗi: Token không hợp lệ", 400

if __name__ == '__main__':
    app.run(debug=True)