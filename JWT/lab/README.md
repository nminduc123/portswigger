# Lab: JWT authentication bypass via unverified signature (Practitioner)

Bài lab này mô phỏng lại bài lab mức độ Practitioner kinh điển của PortSwigger Web Security Academy: **JWT authentication bypass via unverified signature**.

---

## 1. Mục tiêu bài Lab
- Đăng nhập bằng tài khoản người dùng bình thường: `wiener:peter`.
- Tìm lỗ hổng trong cơ chế xử lý JWT của ứng dụng web.
- Leo đặc quyền thành `administrator`.
- Truy cập vào trang quản trị `/admin` và xóa tài khoản người dùng `carlos`.

---

## 2. Cách khởi chạy Lab

Mở PowerShell / Command Prompt tại thư mục lab hoặc thư mục gốc `portswigger`:

### Cách 1: Sử dụng môi trường ảo Python (venv) đã có sẵn trong folder portswigger:
```powershell
cd "C:\Users\vds_minhntd\Downloads\portswigger"
.\venv\Scripts\python.exe "JWT\lab\app.py"
```

### Cách 2: Chạy trực tiếp từ thư mục `lab`:
```powershell
cd "C:\Users\vds_minhntd\Downloads\portswigger\JWT\lab"
python app.py
```

Sau khi chạy thành công, truy cập trình duyệt tại địa chỉ:
👉 **http://127.0.0.1:5000**

---

## 3. Bản chất lỗ hổng trong code (Tại sao bị khai thác?)

Xem trong file `app.py`:
```python
def get_current_user():
    token = request.cookies.get('session')
    # ...
    parts = token.split('.')
    # BỎ QUA signature, chỉ parse payload base64!
    payload_bytes = b64url_decode(parts[1])
    payload = json.loads(payload_bytes.decode('utf-8'))
    return payload.get("sub")
```
- Khi server tạo token cho user, server có ký HMAC-SHA256 với `SECRET_KEY`.
- Nhưng khi **xác thực token** người dùng gửi lên qua cookie `session`, server chỉ tách lấy phần Payload (phần thứ 2 sau dấu chấm), giải mã Base64 và tin tưởng tuyệt đối vào trường `sub` mà **hoàn toàn không kiểm tra tính toàn vẹn của Signature**.

---

## 4. Hướng dẫn khai thác từng bước (Walkthrough)

### Bước 1: Đăng nhập
1. Truy cập `http://127.0.0.1:5000/login`.
2. Đăng nhập với tài khoản:
   - Username: `wiener`
   - Password: `peter`
3. Sau khi đăng nhập, bạn được chuyển đến trang `/my-account`. Kiểm tra cookie `session` (có thể dùng F12 -> tab Storage/Application -> Cookies hoặc bắt trong Burp Suite).

---

### Bước 2: Phân tích & Sửa JWT

Cookie `session` có định dạng: `HEADER.PAYLOAD.SIGNATURE`

Phần **Payload** ban đầu (khi giải mã Base64url):
```json
{"iss":"portswigger-jwt-lab","sub":"wiener","role":"user"}
```

Sử dụng Burp Suite extension **JWT Editor** (hoặc trang web jwt.io / terminal Python / CyberChef):
1. Sửa trường `"sub"` từ `"wiener"` thành `"administrator"`:
```json
{"iss":"portswigger-jwt-lab","sub":"administrator","role":"admin"}
```
2. Mã hóa Base64url lại phần Payload vừa sửa.
3. Ghép lại chuỗi JWT:
   - Giữ nguyên Header ban đầu
   - Thay phần Payload mới vào
   - Giữ nguyên Signature cũ (hoặc để trống, vì server không kiểm tra signature)

---

### Bước 3: Leo quyền Admin và Xóa Carlos
1. Bật Burp Suite Repeater hoặc chỉnh sửa trực tiếp cookie `session` trên trình duyệt bằng giá trị JWT vừa tạo.
2. Truy cập vào đường dẫn:
   ```
   http://127.0.0.1:5000/admin
   ```
3. Lúc này bạn đã truy cập thành công vào **Admin Panel**.
4. Bấm nút **"Xóa người dùng"** bên cạnh tài khoản `carlos` hoặc gửi GET request tới:
   ```
   http://127.0.0.1:5000/admin/delete?username=carlos
   ```
5. Hệ thống hiển thị thông báo:
   🎉 **Congratulations, you solved the lab! User carlos has been deleted.**
