from flask import Flask, request, redirect, make_response
from cryptography.hazmat.primitives.asymmetric import rsa
import jwt
from jwt import PyJWK

app = Flask(__name__)

# Server sinh cặp khóa RSA chuẩn nội bộ để ký token cho người dùng
SERVER_PRIVATE_KEY = rsa.generate_private_key(public_exponent=65537, key_size=2048)
SERVER_PUBLIC_KEY = SERVER_PRIVATE_KEY.public_key()

USERS = {
    "wiener": "peter",
    "carlos": "password123",
    "administrator": "admin_super_pass_999"
}

def create_jwt(username):
    # Server ký token bằng RS256 với khóa Private nội bộ
    headers = {"kid": "server-key-id"}
    return jwt.encode({"sub": username}, SERVER_PRIVATE_KEY, algorithm="RS256", headers=headers)

def verify_jwt(token):
    """
    [PRACTITIONER - JWK HEADER INJECTION]
    Lỗ hổng: Server kiểm tra nếu trong Header của JWT có chứa tham số 'jwk',
    nó sẽ ngây thơ dùng chính Public Key được nhúng trong 'jwk' đó để xác thực chữ ký!
    Kẻ tấn công chỉ cần tạo cặp khóa RSA riêng, nhúng public key vào header và ký token bằng private key của mình.
    """
    if not token:
        return None
    try:
        header = jwt.get_unverified_header(token)

        # ❌ LỖ HỔNG JWK HEADER INJECTION:
        # Nếu client gửi kèm 'jwk', server tin tưởng và lấy public key từ chính client gửi lên!
        if "jwk" in header:
            public_key = PyJWK(header["jwk"]).key
            payload = jwt.decode(token, public_key, algorithms=["RS256"])
            return payload.get("sub")
        else:
            # Ngược lại, xác thực bằng Public Key chuẩn của server
            payload = jwt.decode(token, SERVER_PUBLIC_KEY, algorithms=["RS256"])
            return payload.get("sub")
    except Exception:
        return None

# --- ROUTES ---

@app.route('/', methods=['GET'])
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return '''
            <h2>Đăng nhập (Lab: JWK header injection)</h2>
            <p>Tài khoản: wiener / peter</p>
            <form method="POST" action="/login">
                <input type="text" name="username" value="wiener"><br><br>
                <input type="password" name="password" value="peter"><br><br>
                <button type="submit">Đăng nhập</button>
            </form>
        '''

    username = request.form.get('username')
    password = request.form.get('password')

    if username in USERS and USERS[username] == password:
        resp = make_response(redirect('/my-account'))
        resp.set_cookie('session', create_jwt(username))
        return resp
    return "Sai tài khoản hoặc mật khẩu! <a href='/login'>Thử lại</a>", 401

@app.route('/my-account')
def my_account():
    user = verify_jwt(request.cookies.get('session'))
    if not user:
        return "<h3>401 Unauthorized: Chữ ký RS256 không hợp lệ!</h3><a href='/login'>Đăng nhập lại</a>", 401

    admin_link = '<p><a href="/admin">👉 <b>Trang Admin Panel</b></a></p>' if user == 'administrator' else ''

    return f'''
        <h2>My Account</h2>
        <p>Xin chào: <b>{user}</b></p>
        {admin_link}
        <br><a href="/logout">Đăng xuất</a>
    '''

@app.route('/admin')
def admin():
    user = verify_jwt(request.cookies.get('session'))
    if user != 'administrator':
        return "<h3>401 Unauthorized: Chỉ administrator mới có quyền!</h3><a href='/my-account'>Quay lại</a>", 401

    carlos_status = "<li>carlos - <a href='/admin/delete?username=carlos'>[Xóa carlos]</a></li>" if "carlos" in USERS else "<li>carlos (ĐÃ BỊ XÓA)</li>"

    return f'''
        <h2>Admin Panel</h2>
        <p>Chào admin! Quản lý người dùng:</p>
        <ul>
            {carlos_status}
            <li>wiener</li>
        </ul>
        <br><a href="/my-account">Quay lại My Account</a>
    '''

@app.route('/admin/delete')
def delete_carlos():
    user = verify_jwt(request.cookies.get('session'))
    if user != 'administrator':
        return "401 Unauthorized", 401

    if request.args.get('username') == 'carlos':
        if 'carlos' in USERS:
            del USERS['carlos']
        return "<h2>🎉 Đã xóa carlos thành công! Hoàn thành bài lab JWK Header Injection!</h2><br><a href='/admin'>Quay lại Admin</a>"

    return redirect('/admin')

@app.route('/logout')
def logout():
    resp = make_response(redirect('/login'))
    resp.delete_cookie('session')
    return resp

if __name__ == '__main__':
    app.run(debug=True, port=5000)
