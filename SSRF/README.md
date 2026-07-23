# Mục lục

1. [Lab: Basic SSRF against the local server](#lab-basic-ssrf-against-the-local-server)

2. [Lab: Basic SSRF against another back-end system](#lab-basic-ssrf-against-another-back-end-system)

3. [Lab: Blind SSRF with out-of-band detection](#lab-blind-ssrf-with-out-of-band-detection)

4. [Lab: SSRF with blacklist-based input filter](#lab-ssrf-with-blacklist-based-input-filter)

5. [Lab: SSRF with filter bypass via open redirection vulnerability](#lab-ssrf-with-filter-bypass-via-open-redirection-vulnerability)

6. [Lab: SSRF with whitelist-based input filter](#lab-ssrf-with-whitelist-based-input-filter)
---

# __Lab: Basic SSRF against the local server__

Access Lab, vào 1 sản phẩm bất kì và check stock để Burpsuite có thể bắt được POST /product/stock

![alt text](images/image.png)

Send to Repeater, sửa lại stockAPI thành địa chỉ `http://localhost/admin`

![alt text](images/image-1.png)

Tuy nhiên vì nó sẽ chỉ hiển thị thay vì cho tương tác trực tiếp nên ta sẽ phải thực hiện xóa account carlos từ bên trong. Thêm vào cuối API /delete?usernam=carlos và Send để hoàn thành bài lab.

![alt text](images/image-2.png)


# __Lab: Basic SSRF against another back-end system__

Access Lab, vào 1 sản phẩm bất kì và check stock để Burpsuite có thể bắt được POST /product/stock

![alt text](images/image-3.png)

Trong 1 số trường hợp máy chủ sẽ không thể tương tác với hệ thống nội bộ mà phải truy cập qua 1 địa chỉ IP nhất định. Ở bài này thì địa chỉ IP sẽ là `192.168.0.X:8080`.

![alt text](images/image-4.png)

Send to Intruder, để tìm được địa chỉ IP chính xác. 

![alt text](images/image-5.png)

Khi này Burpsuite sẽ trả về 1 giá trị với status code hợp lệ.

![alt text](images/image-6.png)

Send to Repeater, thay vào giá trị X và tiến hành xóa account carlos từ bên trong và hoàn thành bài lab.

![alt text](images/image-7.png)


# __Lab: Blind SSRF with out-of-band detection__

Access Lab, vào 1 sản phẩm bất kì để Burpsuite bắt được request GET /product?productId

![alt text](images/image-8.png)

Vì bài này server k hề trả về bất cứ 1 response nào ra ngoài giao diện nên ta có thể  dùng Burp Collaborator để kiểm tra liệu server có hói quen đọc `referer` rồi rồi tự động gọi `DNS` hoặc `HTTP` request hay k.

![alt text](images/image-9.png)

Send, khi này ta sẽ có thể thấy được các lượt tương tác DNS và HTTP do ứng dụng khởi tạo từ kết quả của payload.

![alt text](images/image-10.png)

Và bài lab được hoàn thành.

![alt text](images/image-11.png)


# __Lab: SSRF with blacklist-based input filter__


Access Lab, vào 1 sản phẩm bất kì và check stock để Burpsuite có thể bắt được POST /product/stock

![alt text](images/image-12.png)

Send to Repeater, thử kiểm tra bằng cách thay API thành các địa chỉ `/localhost` hoặc `/127.0.0.1` thì thấy bị chặn vì lí do bảo mật. Đây là do server đã liệt 1 vài điểm vào blacklist như là `/admin`,`/localhost` hoặc `/127.0.0.1`

![alt text](images/image-13.png)

Tuy nhiên vẫn có thể vượt qua bộ lọc bằng 1 vài cách như dùng 1 dạng biểu diễn khác cho IP`127.0.0.1` như là `127.1`

![alt text](images/image-14.png)

Để vào được `/admin` ta có thể thử mã hóa 1 số phần để bypass. VD:`admin` = `ad%6din`(URL) = `ad%25%36%64in`

![alt text](images/image-15.png)

Tiến hành xóa account carlos từ bên trong và hoàn thành bài lab.

![alt text](images/image-16.png)


# __Lab: SSRF with filter bypass via open redirection vulnerability__

Access Lab, vào 1 sản phẩm bất kì và check stock để Burpsuite có thể bắt được POST /product/stock. Send to Repeater

![alt text](images/image-17.png)

Đôi khi ta có thể vượt qua bằng cách khai thác các lỗ hổng định tuyến mở. VD: ứng dụng có lỗ hổng chuyển hướng đến 1 URL mà không kiểm soát. Ở trang thông tin sản phẩm ta có thể chuyển hướng sang sản phẩm tiếp theo bằng `Next product`. Click vào để Burpsuite có thể bắt được GET /product/nextProduct

![alt text](images/image-18.png)

Ở đây ta thấy được cấu trúc chuyển từ sản phầm 1 sang sản phâm 2 bằng `/product/nextProduct?currentProductId=1&path=/product?productId=2`. Giả sử nếu như thay vì chuyển sang trang sản phẩm 2 mà chuyển sang 1 trang khác thì sao như là admin thì sao. Sử dụng cấu trúc để chuyển từ trang sản phầm 1 sang trang admin.

![alt text](images/image-19.png)

Tiến hành xóa account carlos từ bên trong và hoàn thành bài lab.

![alt text](images/image-20.png)


# __Lab: SSRF with whitelist-based input filter__

Access Lab, vào một sản phẩm bất kỳ và chọn check stock để Burp Suite có thể bắt được request POST /product/stock

![alt text](images/image-21.png)

Send request đó sang Repeater.Thử sửa tham số stockApi thành `http://localhost/admin `để xem server có bị dính SSRF không. Tuy nhiên, khi bấm Send, ta sẽ nhận được thông báo lỗi **"External stock check host must be stock.weliketoshop.net"**.

![alt text](images/image-22.png)

Để vượt qua hàng rào bảo vệ này, ta có thể thử bypass whitelist bằng cách nhồi thêm tên miền hợp lệ vào sau bằng ký tự mã hóa URL VD: dùng `http://localhost:80#@stock.weliketoshop.net/admin` có thể thử mã hóa `#` để vào được bên trong.

![alt text](images/image-23.png)

Tiến hành xóa account carlos từ bên trong và hoàn thành bài lab.

![alt text](images/image-24.png)