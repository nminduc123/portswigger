# __Lab: Username enumeration via different responses__

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


# __Lab: 2FA simple bypass__

Đăng nhập vào bằng tài khoản wiener

![alt text](images/image-4.png)

Truy cập vào Email Client để lấy mã security

![alt text](images/image-5.png)

Sau đấy Đăng xuất tài khoản cá nhân:wiener và đăng nhập bằng tài khoản carlos. Khi bị hỏi mã xác thực back to labhome và vào lại My Account sẽ thấy đã vượt được xác thực và hoàn thành bài lab

![alt text](images/image-6.png)


# __Lab: Password reset broken logic__

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


# __Lab: Username enumeration via subtly different responses__

Đăng nhập bằng 1 tài khoản bất kì

![alt text](images/image-13.png)

Khi đấy burpsuite sẽ bắt được POST /login

Send to Intruder clear toàn bộ các đánh dấu Payload chỉ Add vào username

![alt text](images/image-14.png)

Nạp các username khả thi vào Payload. Vào settings highlight Invalid username or password. Rồi attacks

![alt text](images/image-15.png)

Sau khi attack burpsuite sẽ trả về 1 warning username khác với phần còn lại thì đấy chính là username cần tìm.

Thay thế username đã biết vào Intruder, đánh dấu Payload password và nạp vào danh sách password khả thi rồi attack

![alt text](images/image-16.png)

Sau khi attack burp sẽ trả về 1 password vs status 302 

![alt text](images/image-17.png)

Quay lại trang đăng nhập và sử dụng username cùng với password đã tìm được và hoàn thành bài lab

![alt text](images/image-18.png)


# __Lab: Username enumeration via response timing__

Truy cập My Account và đăng nhập bằng 1 tài khoản bất kì invalid để burpsuite có thể bắt được POST /login

![alt text](images/image-19.png)

Send to Intruder đánh dấu vị trí Payload, nạp danh sách Payloas và Attack. khi đấy thấy rằng bài lab sẽ chặn IP nếu như invalid quá nhiều trong 1 thời gian ngắn

![alt text](images/image-20.png)

Send to Intruder và Add thêm X-Forwarded-For vào header, thêm đánh dấu Payload vào địa chỉ X-Forwarded-For

![alt text](images/image-21.png)

Chuyển cách tấn công từ Sniper attack sang Pitchfork attack.
Khi này Burp sẽ xác định Payload 1: X-Forwarded-For, Payload 2: username

![alt text](images/image-22.png)

Ở Payload 1 sửa lại Type thành number, Cấu hình lại Number range 

![alt text](images/image-23.png)

Add thêm Payload processing chọn rule prefix và thêm 1.1.1. 

![alt text](images/image-24.png)

Ở Payload 2 nạp danh sách username,Sửa password thành 1 chuỗi kí tự dài để máy chủ tốn nhiều thời gian phản hồi, Sửa maximum concurrent requests là 1 rồi attack

![alt text](images/image-25.png)

Thay username đã tìm được và đánh dấu Payload cho password. Nạp danh sách password rồi Attack. Khi đấy sẽ thấy 1 password với status là 302

![alt text](images/image-26.png)

Quay trở lại lab sử dụng username và password đã tìm được để hoàn thành bài lab

![alt text](images/image-27.png)


# __Lab: Broken brute-force protection, IP block__

Truy cập My Account và đăng nhập bằng 1 tài khoản invalid để Burpsuite có thể bắt được POST /login và trả về respone

![alt text](images/image-28.png)

Vì bài lab sẽ chặn IP nếu nhập sai quá nhiều lần nên có 2 hướng đi
### 1. Add X-Forwarded-For và thay đổi IP sau mỗi lần để tránh bị khóa 
### 2. Dùng spoof để reset sau mỗi lần thử sai

Nhưng vì bài lab muốn hiểu được logic nên dùng cách 2. Tạo danh sách Payload username vs password. 

![alt text](images/image-29.png)
![alt text](images/image-30.png)

Đánh dấu Payload vào username và password, chuyển từ Sniper attack sang Pitchfork attack, nạp danh sách username và password rồi Attack

![alt text](images/image-31.png)

Khi đấy burp sẽ trả về danh sách tài khoản khả thi. Sử dụng username và password vừa tìm được để đăng nhập và hoàn thành bài lab

![alt text](images/image-32.png)


# __Lab: Username enumeration via account lock__

Đăng nhập bằng 1 tài khoản invalid bất kì để Burpsuite có thể bắt được POST /login. Send to Intruder, đánh dấu Payload username và password. Chuyển từ Sniper attack sang cluster bomb, nạp danh sách username ở Payload 1 còn Payload 2 chuyển về Type NULL và set generate 5 payload

![alt text](images/image-33.png)

Attack. Sau khi set generate 5 payload thì burp sẽ lặp lại 1 username 5 lần để xác định được username có tồn tại hay k

![alt text](images/image-34.png)

Thấy được độ dài của username:access dài hơn so với các username khác. Quay trở lại Burpsuite sử dụng username:access nạp danh sách password và attack

![alt text](images/image-35.png)

Burpsuite sẽ trả về password xác định dựa trên độ dài khác.

Quay trở lại bài lab sử dụng username và password vừa tìm được để đăng nhập và hoàn thành bài lab

![alt text](images/image-36.png)


