# __JWT là gì__
### JWT là 1 giá trị cookie lưu trữ thông tin của người dùng và chữ kí của server(thẻ VIP) khi cần gửi req thì đưua thẻ là k ai hỏi j cả.

# __JWT attack__
### JWT attack là khi làm giả vé VIP 

## FORMAT: JWT có 3 phần được chia cắt bởi dấu `.` bào gồm header, payload, signature.

## Các nhánh khác:
1. JWS(JSON Web Signature): ai cũng mở ra xem được payload nếu biết cách giải mã Base64
2. JWE(JSON Web Encryption): mã hóa thành 1 chuỗi riêng cần có key mới giả mã đọc được
3. JWK(JSON Web Key): 1 định dạng chuẩn để biểu diễn mã khóa

# __Lab: JWT authentication bypass via unverified signature__

Access lab, đăng nhập bằng account được cung cấp wiener:peter. Send req `/my-account` to Repeater 

![alt text](images/image.png)

Mục tiêu chính là vào đc admin panel để xóa account carlos. Sửa path payload từ giá trị sub là wiener thành administrator và req thành /admin
![alt text](images/image-1.png)
![alt text](images/image-2.png)

Send sẽ thấy mã trạng thái 200 OK tiến hành xóa account carlos bầng các trỏ trực tiếp trong req `/admin/delete?username=carlos` và hoàn thành bài lab

![alt text](images/image-3.png)
![alt text](images/image-4.png)


# __Lab: JWT authentication bypass via flawed signature verification__

Access lab, đăng nhập bằng account được cung cấp wiener:peter. Send req `/my-account` to Repeater 

![alt text](images/image-5.png)


Mục tiêu chính là vào đc admin panel để xóa account carlos. Sửa path payload từ giá trị sub là wiener thành administrator và req thành /admin

![alt text](images/image-6.png)
![alt text](images/image-7.png)

Send tuy nhiên sẽ nhận đc về mã 401 UNauthorized 

![alt text](images/image-8.png)

Tuy nhiên bài chấp nhận 1 jwt k đc kí có thể thử biến từ hàm băm RSA256 thành none và xóa toàn bộ chữ kí đã được tạo từ trc.

![alt text](images/image-10.png)

Send và hoàn thành baai lab.

![alt text](images/image-11.png)


# __Lab: JWT authentication bypass via weak signing key__

Access lab, đăng nhập bằng account được cung cấp wiener:peter. Send req `/my-account` to Repeater 

![alt text](images/image-12.png)

Mục tiêu chính là vào đc admin panel để xóa account carlos. Sửa path payload từ giá trị sub là wiener thành administrator và req thành /admin

![alt text](images/image-13.png)

Trong bài này ở chữ ký có 1 khóa yếu sử dụng hashcat để tìm ra khóa đó. Thêm 1 wordlist.txt các khóa dễ và lưu cookie chứa toàn bộ `header,payload,sig` vào chung cùng 1 file jwt.txt

![alt text](images/image-14.png)

Sử dụng lệnh `hashcat -a 0 -m 16500 jwt.txt jwt.secrets.list` chạy đợi tìm đợi khóa.

![alt text](images/image-15.png)

Tìm được khóa là secret1 tiến hành tạo 1 chữ ký mới có chứ khóa và payload mong muốn.

![alt text](images/image-16.png)

Lưu vào và sign in repeater.

![alt text](images/image-17.png)

Send và hoàn thàn bài lab.

![alt text](images/image-18.png)


# __Lab: JWT authentication bypass via jwk header injection__

Access lab, đăng nhập bằng account được cung cấp wiener:peter. Send req `/my-account` to Repeater

![alt text](images/image-19.png)

Mục tiêu chính là vào đc admin panel để xóa account carlos. Sửa path payload từ giá trị sub là wiener thành administrator và req thành /admin

![alt text](images/image-20.png)

Để solved được bài cần núng đc jwk vào header. Tạo 1 Key RSA mới với kid giữ nguyên 

![alt text](images/image-21.png)

Lưu và attack đến req khi này các giá trị jkw sẽ được thêm vòa header của req.

![alt text](images/image-22.png)

Send và hoàn thành bài lab.

![alt text](images/image-23.png)


# __Lab: JWT authentication bypass via jku header injection__

Access lab, đăng nhập bằng account được cung cấp wiener:peter. Send req `/my-account` to Repeater

![alt text](images/image-24.png)

Mục tiêu chính là vào đc admin panel để xóa account carlos. Sửa path payload từ giá trị sub là wiener thành administrator và req thành /admin

![alt text](images/image-25.png)

Tạo 1 khóa RSA mới với giá trị kid giữ nguyên. Vì bài này máy chủ có hỗ trợ jku trong header tuy nhiên lại không ktra URL.

Copy public key vừa tạo và dán vào server exploit 

![alt text](images/image-26.png)

Sửa đổi tham số jku trong header để trỏ về server

![alt text](images/image-27.png)

Kí lại chữ kí với key đã tạo và send để hoàn thành bài lab.

![alt text](images/image-28.png)


# __Lab: JWT authentication bypass via kid header path traversal__

Access lab, đăng nhập bằng account được cung cấp wiener:peter. Send req `/my-account` to Repeater

![alt text](images/image-29.png)

Mục tiêu chính là vào đc admin panel để xóa account carlos. Sửa path payload từ giá trị sub là wiener thành administrator và req thành /admin

![alt text](images/image-30.png)



# __Lab: JWT authentication bypass via algorithm confusion__

Access lab, đăng nhập bằng account được cung cấp wiener:peter. Send req `/my-account` to Repeater

![alt text](images/image-31.png)

Mục tiêu chính là vào đc admin panel để xóa account carlos. Sửa path payload từ giá trị sub là wiener thành administrator và req thành /admin

![alt text](images/image-32.png)

Trong 1 số trường hợp cá key public của server sẽ được lưu ở các endpoint có dạng `/jwks.json`

![alt text](images/image-33.png)

Tạo 1 Key RSA mới với chung kid tuy nhiên sử dụng key public để coi như tạo ra 1 key private mới

![alt text](images/image-34.png)

Về repeater attack req với key mới và chuyển định dạng sang HMAC để coi như là 1 key mới hoàn toàn. Send và hoàn thành bài lab.

![alt text](images/image-35.png)