# PortSwigger Clone: File Upload Vulnerability Lab

## Giới thiệu
Đây là môi trường lab local mô phỏng lại bài tập về lỗ hổng File Upload trên PortSwigger Web Security Academy. Lab cung cấp một ứng dụng web PHP có chức năng upload file nhưng thiếu cơ chế validate an toàn, cho phép thực hành các kỹ thuật bypass và leo thang đặc quyền.

## Cấu trúc thư mục
* `login.php` / `logout.php` / `users.php`: Chức năng xác thực người dùng.
* `upload.php`: Endpoint chính xử lý file upload (điểm khai thác lỗ hổng).
* `uploads/`: Thư mục lưu trữ file sau khi được tải lên hệ thống.
* `shell.php`: Payload mẫu (Web shell) dùng để test RCE.

## Yêu cầu hệ thống
* Web Server hỗ trợ PHP (Khuyến nghị sử dụng **XAMPP**).

## Hướng dẫn triển khai

1. Clone repository này về máy local.

2. Copy toàn bộ thư mục mã nguồn vào thư mục root của Web Server (Ví dụ: `C:\xampp\htdocs\tên-thư-mục` đối với XAMPP).

3. Mở XAMPP Control Panel và khởi động dịch vụ **Apache**.

4. Truy cập vào ứng dụng qua trình duyệt: `http://localhost/tên-thư-mục/login.php`

## Mục tiêu
Bypass cơ chế filter tại `upload.php` để tải thành công file `shell.php` (hoặc payload tùy chỉnh) lên thư mục `uploads/`. Sau đó, truy cập trực tiếp vào file mã độc vừa upload để đạt được Remote Code Execution (RCE).