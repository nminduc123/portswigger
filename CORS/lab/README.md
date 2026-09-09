# CORS Null Origin Lab

Lab local mô phỏng lỗ hổng **CORS với trusted `null` origin**, lấy ý tưởng từ PortSwigger Web Security Academy.

> ⚠️ Lab này chỉ chạy trên máy local, sử dụng tài khoản và dữ liệu giả.

---

## 1. Mục tiêu

Mục tiêu của lab là hiểu và thực hành:

- CORS
- `Origin: null`
- `Access-Control-Allow-Origin`
- `Access-Control-Allow-Credentials`
- Session Cookie
- `SameSite`
- `Secure`
- Sandboxed iframe
- Burp Suite
- Attacker server
- Cách dữ liệu API có thể bị đọc khi CORS cấu hình sai

Attack flow:

```text
Burp Suite
     |
     | Origin: null
     v
Vulnerable Server
     |
     | CORS misconfiguration
     v
Attack Panel
     |
     v
Fake Mail
     |
     v
Malicious Page
     |
     v
Sandboxed iframe
     |
     | Origin: null
     v
/ api/accountDetails
     |
     v
Fake Victim Data
     |
     v
Attacker Server