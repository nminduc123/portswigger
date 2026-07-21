# __Lab: Excessive trust in client-side controls__

Access Lab, đăng nhập bằng account wiener:peter. Bật Intercept trên BurpSuite để có thể chặn được POST /cart khi thêm áo l33t vào giỏ hàng.

![alt text](images/image.png)

Nhận thấy có price ở request thử thay đổi giá của áo rồi forward để gửi về server. Vào giỏ hàng kiểm tra thì thấy giá đã được thay đổi.

![alt text](images/image-1.png)

Tiến hành thanh toán và hoàn thành bài lab.

![alt text](images/image-2.png)


# __Lab: High-level logic vulnerability__

Access Lab, đăng nhập bằng account wiener:peter. Bật Intercept trên BurpSuite để có thể chặn được POST /cart khi thêm áo l33t vào giỏ hàng.

![alt text](images/image-3.png)

Thử thay đổi giá trị quantity thành giá trị âm và forwrad khi này số lượng áo ở trang và total price đều chuyển về âm.

![alt text](images/image-4.png)

Loại bỏ áo khỏi giỏ hàng thêm vật phẩm khác vào giỏ hàng dùng Burpsuite chặn và chuyển số lường về âm. Sao cho đế khi total price của cả áo và các vật phẩm khác đủ với số tiền đang sở hữu.

![alt text](images/image-5.png)

Tiến hành thanh toán và hoàn thành bài lab.

![alt text](images/image-6.png)


# __Lab: Inconsistent security controls__

Access Lab, nhận thấy có thể tự đăng kí 1 tài khoản cá nhân. Truy cập vào email client để lấy được đường dẫn email.

![alt text](images/image-7.png)

Sử dụng email và đăng kí. 

![alt text](images/image-8.png)

Quay trở lại email để xác thực đăng kí thành công. Đăng nhập vào account vừa tạo. Nhận thấy có phần thay đổi email vì email đã được xác thực và đăng kí thành công, thay đổi đuôi email thành `@dontwannacry.com`

![alt text](images/image-9.png)

Vì chỉ khi sử dụng email của dontưannacry mới có quyền truy cập admin. Sau khi đỏi thành công email thì bây giờ account của ta có thêm admin panel.

![alt text](images/image-10.png)

Truy cập và xóa account carlos để hoàn thành bài lab.

![alt text](images/image-11.png)


# __Lab: Flawed enforcement of business rules__

Access Lab, đăng nhập bằng account wiener:peter. Nhận thấy có 2 mã giảm giá: `NEWCUST5` và 1 mã khi đăng kí bằng email `SIGNUP30`. Thêm áo vào giỏ hàng và add mã giảm giá.

![alt text](images/image-12.png)

Tuy nhiên khi add lại cùng 1 mã vừa add thì sẽ được báo là "mã đã được sử dụng" nhưng add một mã khác kể cả là mã đã add trước đó nữa thì hệ thống nhận nhận và giảm giá.

![alt text](images/image-13.png)

Liên tục thay đổi và add mã vào cho đến khi total price giảm đến mức vừa đủ với số tiền đang sở hữu.

![alt text](images/image-14.png)

Tiến hành thanh toán và hoàn thành bào lab.

![alt text](images/image-15.png)