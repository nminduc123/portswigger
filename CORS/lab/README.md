CORS Null Origin Lab

Deployment Guide

Lab mô phỏng lỗ hổng CORS với null origin trong môi trường local.

Architecture

Vulnerable Server: https://localhost:3000

Attacker Server: http://localhost:4000

Database: MySQL

Database name: cors_null_lab

Attack flow:

Victim Login
     ↓
Session Cookie
     ↓
Fake Email
     ↓
malicious.html
     ↓
Sandboxed iframe
     ↓
Origin: null
     ↓
Vulnerable API
     ↓
Victim Data
     ↓
Attacker Server

Lab này chỉ sử dụng dữ liệu giả và môi trường local.

1. Requirements

Cài các phần mềm sau:

Git

Node.js

XAMPP

Burp Suite

mkcert

Chrome/Chromium

Kiểm tra Node.js:

node -v
npm -v

Kiểm tra mkcert:

mkcert -version

2. Clone Repository

Clone repository:

git clone <GITHUB_REPOSITORY_URL>

Di chuyển vào project:

cd <PROJECT_FOLDER>

Ví dụ:

cd E:\portswigger\CORS\lab

Kiểm tra project:

tree /F

Project phải có các thư mục chính:

lab/
├── database/
├── vulnerable-server/
└── attacker-server/

3. Setup MySQL

3.1. Start XAMPP

Mở XAMPP Control Panel.

Start:

MySQL

Có thể start Apache nếu cần sử dụng phpMyAdmin:

Apache

3.2. Mở phpMyAdmin

Truy cập:

http://localhost/phpmyadmin

3.3. Import database

Trong repository đã có:

database/init.sql

Trong phpMyAdmin:

SQL

Mở file:

database/init.sql

Copy nội dung file vào SQL editor rồi Execute.

Sau khi import thành công phải có:

cors_null_lab
└── users

Database có sẵn các tài khoản phục vụ lab:

victim
attack

4. Setup Vulnerable Server

Di chuyển vào thư mục:

cd vulnerable-server

Cài dependencies:

npm install

Sau khi cài xong phải có:

node_modules/
package-lock.json

5. Configure .env

Kiểm tra file:

vulnerable-server/.env

Cấu hình mặc định:

DB_HOST=localhost
DB_PORT=3306
DB_USER=root
DB_PASSWORD=
DB_NAME=cors_null_lab

PORT=3000

Nếu MySQL của bạn có password cho root, sửa:

DB_PASSWORD=<MYSQL_PASSWORD>

Không commit password thật lên GitHub.

6. Setup HTTPS

Vulnerable Server sử dụng HTTPS vì session cookie được cấu hình:

SameSite=None
Secure=true

Do đó cần tạo certificate local bằng mkcert.

6.1. Install local CA

Chạy:

mkcert -install

6.2. Tạo certificate

Di chuyển vào:

cd vulnerable-server

Chạy:

mkcert localhost 127.0.0.1 ::1

Sau đó kiểm tra:

dir

Phải có certificate và private key tương ứng với tên mà server.js đang sử dụng.

Ví dụ:

localhost+2.pem
localhost+2-key.pem

Nếu tên file khác với tên được khai báo trong server.js, đổi tên file hoặc cập nhật đường dẫn trong server.js.

7. Start Vulnerable Server

Từ thư mục:

vulnerable-server

chạy:

npm start

Hoặc:

node server.js

Nếu thành công sẽ hiển thị:

https://localhost:3000

Giữ terminal này chạy.

8. Setup Attacker Server

Mở một terminal mới.

Quay lại project:

cd <PROJECT_FOLDER>

Ví dụ:

cd E:\portswigger\CORS\lab

Di chuyển vào:

cd attacker-server

Cài dependencies:

npm install

9. Start Attacker Server

Chạy:

npm start

Hoặc:

node server.js

Nếu thành công sẽ hiển thị:

http://localhost:4000

Giữ terminal này chạy.

10. Verify Deployment

Lúc này phải có hai server đang chạy.

Vulnerable Server

https://localhost:3000

Attacker Server

http://localhost:4000

Mở trình duyệt và kiểm tra:

https://localhost:3000

và:

http://localhost:4000

Nếu cả hai truy cập được thì deployment cơ bản đã hoàn tất.

11. Login Victim

Truy cập:

https://localhost:3000/login

Sử dụng tài khoản:

Username: victim
Password: victim123

Sau khi login thành công, kiểm tra session cookie:

F12
→ Application
→ Cookies
→ https://localhost:3000

Cookie session phải tồn tại.

12. Verify API

Sau khi đăng nhập, truy cập:

https://localhost:3000/api/accountDetails

API phải trả về thông tin tài khoản victim.

Ví dụ:

{
    "username": "victim",
    "email": "victim@example.com",
    "apiKey": "VICTIM-SECRET-98765"
}

Nếu nhận:

{
    "error": "Not authenticated"
}

hãy kiểm tra lại session cookie.

13. Test CORS

Mở Burp Suite.

Bật:

Proxy → Intercept

Truy cập:

https://localhost:3000/api/accountDetails

Trong request thêm:

Origin: null

Ví dụ:

GET /api/accountDetails HTTP/1.1
Host: localhost:3000
Origin: null

Gửi request.

14. Verify Vulnerable CORS Configuration

Kiểm tra response.

Lab vulnerable phải trả:

Access-Control-Allow-Origin: null
Access-Control-Allow-Credentials: true

Điều này chứng minh server đang tin tưởng:

Origin: null

Nếu response không có:

Access-Control-Allow-Origin: null

hãy kiểm tra lại cấu hình CORS trong source code.

15. Attack Panel

Mở:

http://localhost:4000/attack.html

Attack Panel dùng để:

Xem target API

Xem cấu hình CORS

Xem payload

Tham khảo attack flow

Không dùng attack.html để tạo Origin: null trực tiếp.

Lý do:

attack.html
      ↓
http://localhost:4000

nên origin của nó là:

http://localhost:4000

Để tạo:

Origin: null

lab sử dụng sandboxed iframe trong:

malicious.html

16. Execute Attack

Step 1 — Open Fake Email

Truy cập:

http://localhost:4000/mail.html

Step 2 — Click Email Link

Click:

View your account information

Trang sẽ chuyển tới:

http://localhost:4000/malicious.html

Step 3 — Trigger Payload

Trong malicious.html, click:

View your account information

Payload sẽ tạo sandboxed iframe.

Iframe sử dụng:

sandbox="allow-scripts"

và không có:

allow-same-origin

Do đó document bên trong iframe có:

Origin: null

17. Verify Attack in Burp

Mở:

Proxy → HTTP history

Tìm:

GET /api/accountDetails

Kiểm tra request.

Phải thấy:

Origin: null

Nếu session được gửi, request cũng sẽ chứa session cookie.

Kiểm tra response:

HTTP/1.1 200 OK
Access-Control-Allow-Origin: null
Access-Control-Allow-Credentials: true

Response body sẽ chứa dữ liệu của victim.

18. Verify Data Received by Attacker

Quay lại terminal đang chạy:

attacker-server

Endpoint:

POST /log

sẽ nhận dữ liệu.

Nếu attack thành công, terminal sẽ hiển thị dữ liệu victim.

Ví dụ:

[+] Data received:
{
    username: 'victim',
    email: 'victim@example.com',
    apiKey: 'VICTIM-SECRET-98765'
}

19. Attack Success Criteria

Không coi attack là thành công chỉ vì malicious.html mở được.

Attack thành công khi tất cả điều kiện sau đúng:

[✓] Victim đã login
[✓] Session cookie tồn tại
[✓] Request tới /api/accountDetails
[✓] Request có Origin: null
[✓] Session được gửi
[✓] Server trả HTTP 200
[✓] Response chứa dữ liệu victim
[✓] Attacker server nhận được dữ liệu qua /log

Nếu:

Origin: null

nhưng server trả:

401 Unauthorized

thì attack chưa thành công.

20. Troubleshooting

20.1. 401 Not authenticated

Kiểm tra:

Đã login victim chưa.

Đang sử dụng HTTPS chưa.

Session cookie có tồn tại không.

Request có gửi cookie không.

Cookie có SameSite=None không.

Cookie có Secure=true không.

Vulnerable Server phải sử dụng:

https://localhost:3000

Không sử dụng:

http://localhost:3000

với session cookie Secure=true.

20.2. Request không có Cookie

Mở:

F12
→ Application
→ Cookies
→ https://localhost:3000

Kiểm tra session cookie.

Sau đó mở Burp:

Proxy
→ HTTP history

Kiểm tra request tới:

/api/accountDetails

Nếu request không có cookie, kiểm tra lại:

SameSite=None
Secure=true

và đảm bảo server đang chạy HTTPS.

20.3. Origin không phải null

Nếu thấy:

Origin: http://localhost:4000

thì request đang chạy trực tiếp từ attacker server.

Để tạo:

Origin: null

phải thực hiện payload từ sandboxed iframe trong:

malicious.html

Không thêm:

allow-same-origin

vào sandbox.

20.4. CORS không trả header

Kiểm tra cấu hình CORS trong source code.

Lab phải cho phép:

null

Sau khi sửa source code, restart server:

Ctrl + C
npm start

20.5. Certificate Error

Chạy:

mkcert -install

Sau đó tạo lại certificate:

cd vulnerable-server
mkcert localhost 127.0.0.1 ::1

Kiểm tra lại các file certificate.

Restart server:

npm start

20.6. MySQL Connection Error

Kiểm tra XAMPP:

MySQL → Running

Kiểm tra database:

cors_null_lab

Kiểm tra table:

users

Kiểm tra .env:

DB_HOST=localhost
DB_PORT=3306
DB_USER=root
DB_PASSWORD=
DB_NAME=cors_null_lab

Nếu MySQL có password, cập nhật DB_PASSWORD.

20.7. Port 3000 đã được sử dụng

Kiểm tra:

netstat -ano | findstr :3000

Nếu cần dừng process:

taskkill /PID <PID> /F

Sau đó chạy lại:

npm start

20.8. Port 4000 đã được sử dụng

Kiểm tra:

netstat -ano | findstr :4000

Nếu cần dừng process:

taskkill /PID <PID> /F

Sau đó chạy lại attacker server.

21. Reset Database

Nếu muốn reset database về trạng thái ban đầu:

Mở:

http://localhost/phpmyadmin

Import lại:

database/init.sql

Sau đó restart Vulnerable Server:

Ctrl + C
npm start

Đăng nhập lại:

Username: victim
Password: victim123

22. Quick Start

Sau khi đã setup hoàn chỉnh lần đầu, những lần sau chỉ cần:

Terminal 1

cd <PROJECT_FOLDER>\vulnerable-server
npm start

Terminal 2

cd <PROJECT_FOLDER>\attacker-server
npm start

Sau đó:

1. Mở https://localhost:3000/login
2. Login victim / victim123
3. Mở http://localhost:4000/mail.html
4. Click link trong fake email
5. Click link trong malicious.html
6. Mở Burp → HTTP history
7. Kiểm tra Origin: null
8. Kiểm tra HTTP 200
9. Kiểm tra dữ liệu tại attacker-server

23. Final Deployment Checklist

Environment
[ ] Node.js installed
[ ] XAMPP installed
[ ] Burp Suite installed
[ ] mkcert installed

Database
[ ] MySQL running
[ ] cors_null_lab created
[ ] users table created
[ ] victim account exists

Vulnerable Server
[ ] npm install completed
[ ] .env configured
[ ] HTTPS certificate created
[ ] Server running on port 3000

Attacker Server
[ ] npm install completed
[ ] Server running on port 4000

Authentication
[ ] victim login successful
[ ] session cookie exists
[ ] /api/accountDetails works

CORS
[ ] Origin: null accepted
[ ] Access-Control-Allow-Origin: null
[ ] Access-Control-Allow-Credentials: true

Attack
[ ] mail.html works
[ ] malicious.html works
[ ] sandbox iframe created
[ ] Request contains Origin: null
[ ] Session is sent
[ ] API returns HTTP 200
[ ] Attacker server receives data

24. Lab URLs

ComponentURL



Vulnerable Server

https://localhost:3000

Login

https://localhost:3000/login

Account API

https://localhost:3000/api/accountDetails

Attacker Server

http://localhost:4000

Attack Panel

http://localhost:4000/attack.html

Fake Email

http://localhost:4000/mail.html

Malicious Page

http://localhost:4000/malicious.html

25. Lab Credentials

UsernamePassword



victim

victim123

attack

attack123

Các tài khoản và dữ liệu trên chỉ dành cho lab local.

26. Expected Result

Khi deployment và attack hoạt động đúng:

https://localhost:3000
        │
        │ Login
        ▼
     Victim
        │
        │ Session
        ▼
http://localhost:4000/mail.html
        │
        │ Click
        ▼
malicious.html
        │
        │ sandbox iframe
        ▼
    Origin: null
        │
        ▼
/api/accountDetails
        │
        │ authenticated request
        ▼
    HTTP 200
        │
        ▼
    Victim Data
        │
        ▼
      /log
        │
        ▼
Attacker Server

Deployment được coi là hoàn tất khi toàn bộ flow trên hoạt động và Burp có thể xác nhận:

Origin: null

cùng với response:

Access-Control-Allow-Origin: null
Access-Control-Allow-Credentials: true