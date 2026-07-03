Lab: Username enumeration via different responses

Cấu hình proxy, rồi bật intercept on.

Nhập username và password bất kì để burp chặn được

Request /login 

![alt text](images/image.png)

Send to Intruder, loại bỏ tất cả các đánh dấu Payload và Add đánh dấu vào username

![alt text](images/image-2.png)

Copy toàn bộ các user khả thi và Dán vào Payload configuration rồi Attack

Thấy được lengths của username:accounts là 3345

accounts chính là username hợp lệ

Trở lại Intruder loại bỏ vị trí đánh dấu Payload ở username và Add vào password

![alt text](images/image-3.png)

Clear toàn bộ các username khả thi và thay bằng password khả thi vào Payload configuration rồi Attack

Khi đấy burp sẽ trả về password:aaaaaa vs status 302 và length 3345

trở lại lab và nhập username cùng với password để hoàn thành bài lab

![alt text](images/image-1.png)


Lab: 2FA simple bypass

Đăng nhập vào bằng tài khoản wiener

![alt text](images/image-4.png)

Truy cập vào Email Client để lấy mã security

![alt text](images/image-5.png)

Sau đấy Đăng xuất tài khoản cá nhân:wiener và đăng nhập bằng tài khoản carlos. Khi bị hỏi mã xác thực back to labhome và vào lại My Account sẽ thấy đã vượt được xác thực và hoàn thành bài lab

![alt text](images/image-6.png)


Lab: Password reset broken logic

Sử dụng forgot password và dùng username wiener submit

![alt text](images/image-7.png)

Truy cập vào email để lấy link thay đổi password 

![alt text](images/image-8.png)

Thay đổi password thành password bản thân muốn và submit.

![alt text](images/image-9.png)

Khi này burpsuite sẽ bắt được POST /forgot-password?temp-forgot-password-token

![alt text](images/image-10.png)

Send to Repeter để sửa username từ wiener thành carlos và send

![alt text](images/image-11.png)

Quay trở lại trang đăng nhập và đăng nhập bằng tài khoản carlos vs password đã đởi và hoàn thành bài lab

![alt text](images/image-12.png)


Lab: Username enumeration via subtly different responses

Đăng nhập bằng 1 tài khoản bất kì

![alt text](image.png)

Khi đấy burpsuite sẽ bắt được POST /login

Send to Intruder clear toàn bộ các đánh dấu Payload chỉ Add vào username

![alt text](image-1.png)

Nạp các username khả thi vào Payload. Vào settings highlight Invalid username or password. Rồi attacks

![alt text](image-2.png)

Sau khi attack burpsuite sẽ trả về 1 warning username khác với phần còn lại thì đấy chính là username cần tìm.

Thay thế username đã biết vào Intruder, đánh dấu Payload password và nạp vào danh sách password khả thi rồi attack

![alt text](image-3.png)

Sau khi attack burp sẽ trả về 1 password vs status 302 

![alt text](image-4.png)

Quay lại trang đăng nhập và sử dụng username cùng với password đã tìm được và hoàn thành bài lab

![alt text](image-5.png)