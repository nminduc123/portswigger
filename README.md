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

Sử dụng forgot password và dùng username wiener 



Truy cập vào email để lấy link thay đổi password 



Thay đổi password thành password bản thân muốn và submit.



Khi này burpsuite sẽ bắt được POST /forgot-password?temp-forgot-password-token



Send to Repeter để sửa username thành carlos và send



Quay trở lại trang đăng nhập và đăng nhập bằng tài khoản carlos vs password đã đởi và hoàn thành bài lab

