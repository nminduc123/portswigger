# __Lab: File path traversal, simple case__

Access Lab, Bật Intercept và truy cập vào 1 bài viết bats kì để Burpsuite chặn được GET /image?filename

![alt text](images/image.png)

Send to Repeater, sửa đổi filename=43.jpg thành filename=../../../etc/passwd

![alt text](images/image-1.png)

Send để hoàn thành bài lab

![alt text](images/image-2.png)


# __Lab: File path traversal, traversal sequences blocked with absolute path bypass__

Access Lab, Bật Intercept và truy cập vào 1 bài viết bất kì để Burpsuite chặn được GET /image?filename

![alt text](images/image-3.png)

Send to Repeater, sửa đổi filename=56.jpg thành filename=/etc/passwd. Vì hệ thống chặn quyền sửa đổi, di chuyển từ người dùng nhưng lại có thể trích dẫn trực tiếp từ gôc hệ thống tệp.

![alt text](images/image-4.png)

Send để hoàn thành bài lab

![alt text](images/image-5.png)


# __Lab: File path traversal, traversal sequences stripped non-recursively__

Access Lab, Bật Intercept và truy cập vào 1 bài viết bats kì để Burpsuite chặn được GET /image?filename

![alt text](images/image-6.png)

Send to Repeater, sửa đổi filename=17.jpg thành filename=....//....//....//etc/passwd. Vì hệ thống bài lab chỉ quét và xóa chuỗi ../ nên lồng thêm 1 chuỗi ../ vào chung để tạo thành ....// và bypasss

![alt text](images/image-7.png)

Send để hoàn thành bài lab

![alt text](images/image-8.png)


# __Lab: File path traversal, traversal sequences stripped with superfluous URL-decode__

Access Lab, Bật Intercept và truy cập vào 1 bài viết bats kì để Burpsuite chặn được GET /image?filename

![alt text](images/image-9.png)

Send to Repeater, sửa đổi filename=68.jpg thành filename=..%252f..%252f..%252fetc/passwd. Mã hóa 2 lần / thành %2f, % thành %25

![alt text](images/image-10.png)

Send để hoàn thành bài lab

![alt text](images/image-11.png)


# __Lab: File path traversal, validation of start of path__

Access Lab, Bật Intercept và truy cập vào 1 bài viết bats kì để Burpsuite chặn được GET /image?filename

![alt text](images/image-12.png)

Send to Repeater, sửa đổi filename=/var/www/images/45.jpg thành filename=/var/www/images/../../../etc/passwd. Nhiều khi hệ thống sẽ set cố định từ tên tệp gốc có sẵn.

![alt text](images/image-13.png)

Send để hoàn thành bài lab

![alt text](images/image-14.png)


# __Lab: File path traversal, validation of file extension with null byte bypass__

Access Lab, Bật Intercept và truy cập vào 1 bài viết bats kì để Burpsuite chặn được GET /image?filename

![alt text](images/image-15.png)

Send to Repeater, sửa đổi filename=34.jpg thành filename=../../../etc/passwd%00.png. Vì hệ thống sẽ chỉ nhận và kết thúc bằng 1 phần mở rộng đã set như jpg hay png. Lúc này sẽ sử dụng thêm NULL vào để kết thúc đường dẫn bằng phần cần thiết.

![alt text](images/image-16.png)

Send để hoàn thành bài lab

![alt text](images/image-17.png)