import time
import random

# Danh sách 30 mật khẩu khả thi của bạn
PASSWORD_LIST = [
    "123123", "abc123", "football", "monkey", "letmein", "shadow", "master", 
    "666666", "qwertyuiop", "123321", "mustang", "123456", "password", 
    "12345678", "qwerty", "123456789", "12345", "1234", "111111", 
    "1234567", "dragon", "1234567890", "michael", "x654321", "superman", 
    "1qaz2wsx", "baseball", "7777777", "121212", "000000"
]

# Random một mật khẩu từ danh sách trên
current_password = random.choice(PASSWORD_LIST)

# In ra terminal để bạn (người tạo lab) biết mật khẩu đúng của lần chạy này là gì
print(f"[*] Server đã khởi động. Mật khẩu đúng cho 'minh' lần này là: {current_password}")

# Giả lập Database với tính năng khóa tài khoản
users_db = {
    "minh": {
        "password": current_password, 
        "failed_attempts": 0,
        "lockout_until": 0
    }
}

def get_user(username):
    if username in users_db:
        return users_db[username]
    return None

def verify_password(username, password):
    # Thời gian xử lý tạo ra Race Condition
    time.sleep(0.5) 
    if username in users_db and users_db[username]["password"] == password:
        return True
    return False