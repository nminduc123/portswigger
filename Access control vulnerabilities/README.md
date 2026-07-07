# __Lab: Unprotected admin functionality__

Access Lab, thêm robots.txt vào URL 

![alt text](images/image.png)

Sẽ có được đuôi để vào được Account admin. Thay thế robots.txt để vào admin panel, delete account carlos và hoàn thành bài lab

![alt text](images/image-1.png)


# __Lab: Unprotected admin functionality with unpredictable URL__

Access Lab, kiểm tra bằng việc thêm đuôi robots.txt vào URL

![alt text](images/image-2.png)

Khi trả về là 404 thử lại bằng cách kiểm tra source của trang 

![alt text](images/image-3.png)

Thấy được đuôi truy cập admin panel thêm vào URL, để truy cập và xóa acccount carlos

![alt text](images/image-4.png)


# __Lab: User role controlled by request parameter__

Kiểm tra /robots.txt(404 Not Found), kiểm tra /admin 

![alt text](images/image-5.png)

Server chỉ cho phép quyền sau khi đăng nhập. Truy cập và đăng nhập bằng tài khoản khả thi. Bật Intercept trên Burpsuite và load lại trang khi này Burp sẽ chặn được Request GET /my-account?id=wiener 

![alt text](images/image-6.png)

Sửa đổi Admin=false thành Admin=true rồi Forwward để cấp quyền Admin cho account wiener. Khi này account wiener đã có mục Admin Panel, truy cập và tiếp đục chặn và sửa Admin=false, Forward

![alt text](images/image-7.png)

Để có thể truy cập vào và xóa account carlos. Khi xóa account carlos vẫn cần sửa Admin lần nữa để hoàn thành bài lab

![alt text](images/image-8.png)
![alt text](images/image-9.png)
![alt text](images/image-10.png)


# __Lab: User role can be modified in user profile__

Kiểm tra /robots.txt(404 Not Found), kiểm tra /admin server chỉ cho phép quyền sau khi đăng nhập và chỉ khả thi với cá user có roleid=2

![alt text](images/image-11.png)

Đầu tiên đăng nhập bằng tài khoản khỉa thi wiener:peter, Update 1 email mói bất kì và dùng Burp để bắt được POST /my-account/change-email

![alt text](images/image-12.png)

Send to Repeater kiểm tra lại và biết được account wiener có roleid:1 

![alt text](images/image-13.png)

Thêm "roleid":2 vào Request và send lại.

![alt text](images/image-14.png) 

Bây giờ account wiener đã được sửa roleid thành 2 và có quyền Admin. Truy cập Admin panel để xóa account carlos và hoàn thành bài lab

![alt text](images/image-15.png)



# __Lab: User ID controlled by request parameter__

Access Lab, đăng nhập bằng tài khoản khả thi wiener:peter. Dùng Burpsuite để bắt được GET /my-account?id=wiener

![alt text](images/image-16.png)

Send to Repeater và sứa đổi id từ wiener thành carlos va send. Khi này respone sẽ trả về source của trang account của carlos và có được API

![alt text](images/image-17.png)

Sử dụng API của carlos để Submit và hoàn thành bài lab

![alt text](images/image-18.png)


# __Lab: User ID controlled by request parameter, with unpredictable user IDs__

Access Lab, Kiểm tra các blog và tìm thấy được blog của carlos

![alt text](images/image-19.png)

Sử dụng Burpsuite để bắt được GET /blogs?userId

![alt text](images/image-20.png)

Có được userID của carlos. Đăng nhập bằng account khả thi wiener:peter.
Bắt được GET /my-account?id với id của wiener Send to Repeater thay thế id của wiener bằng id của carlos đã có và send. Response sẽ trả về source của trang account của carlos và có được API

![alt text](images/image-21.png)

Sử dụng API đã có để submit và hoàn thành bài lab

![alt text](images/image-22.png)
![alt text](images/image-23.png)


# __Lab: User ID controlled by request parameter with data leakage in redirect__

Access Lab, đăng nhập bằng tài khoản khả thi wiener:peter. Dùng Burpsuite để bắt được GET /my-account?id=wiener

![alt text](images/image-24.png)

Send to Repeater và sứa đổi id từ wiener thành carlos va send. Khi này respone sẽ trả về source của trang account của carlos và có được API

![alt text](images/image-25.png)

Sử dụng API của carlos để Submit và hoàn thành bài lab

![alt text](images/image-26.png)


# __Lab: User ID controlled by request parameter with password disclosure__

Access Lab, đăng nhập bằng tài khoản khả thi wiener:peter. Dùng Burpsuite để bắt được GET /my-account?id=wiener

![alt text](images/image-27.png)

end to Repeater và sứa đổi id từ wiener thành administrator và send. Khi này respone sẽ trả về source của trang account của administrator 

![alt text](images/image-28.png)

Có được value password của account administrator

![alt text](images/image-29.png)

Đăng xuất khỏi account wiener và dùng password vừa lấy được để truy cập vào account admin, delete account carlos và hoàn thành bài lab

![alt text](images/image-30.png)


# __Lab: Insecure direct object references__

Access Lab, truy cập live chat và trò chuyện Hal Pline. Nhận thấy rằng mỗi lần view transcript. Giá trị sẽ tăng dần lên 

![alt text](images/image-31.png)

Nhưng file .txt của lần transcipt đầu tiên lại là 2.txt. Send to repeater và thử sửa giá trị thành 1.txt rồi send

![alt text](images/image-32.png)

Sẽ có được password của account carlos. Đăng nhập vào account carlos và hoàn thành bài lab

![alt text](images/image-33.png)


# __Lab: URL-based access control can be circumvented__

Access Lab, khi access thấy được rằng có thể truy cập vào admin panel. Nhưng khi truy cập thì xuất hiện access denied. 

![alt text](images/image-34.png)

Điều này chúng tỏ front-end đã chặn tương tác vói quyền admin nhưng back-end thì không. Quay trở lại trang chính của bài Lab, Send to Repeater GET / HTTP/2.
Vì back-end có hỗ trọ cho X-Original-URL, add thêm /admin vào và send để có thể lấy được quyền admin.

![alt text](images/image-35.png)

Vì front-end chặn nên bắt buộc phải delete account carlos bằng back-end. Đẻ có thể delete được accouont carlos add thêm /delete cùng với username account cần xóa. 

![alt text](images/image-36.png)

Send để hoàn thành bài lab

![alt text](images/image-37.png)


# __Lab: Method-based access control can be circumvented__

Access Lab, sử dụng account admin để đăng nhập và nâng cấp quyền hạn cho account carlos

![alt text](images/image-38.png)

Sử dụng Burpsuite để bắt được POST /admin-role, Send to Repeater. Đăng xuất khỏi account admin và vào lại bằng account wiener:peter. Khi này Burpsuite sẽ bắt được GET /my-account?id=wiener cũng với cookie khi đăng nhập. 

![alt text](images/image-39.png)

Quay trở lại sửa lại cookie và username thành cookie khi đăng nhập acc wiener và username:wiener

![alt text](images/image-40.png)

Khi send response sẽ trả về Unauthorized. Change request method để chuyển từ POST thành GET và send.

![alt text](images/image-41.png)

Lúc đấy account wiener sẽ được upgrade quyền admin và hoàn thành bài lab

![alt text](images/image-42.png)


# __Lab: Multi-step process with no access control on one step__

Access Lab, sử dụng account admin để đăng nhập và nâng cấp quyền hạn cho account carlos

![alt text](images/image-43.png)

Khi này server sẽ hỏi là có chắc chán muốn sửa đổi quyền hạn hay không

![alt text](images/image-44.png)

Sau khi Đồng Ý hoặc Không thì dùng Burpsuite bắt POST /admin-roles HTTP/2 và Send to Repeater. Đăng xuất khỏi account admin và vào lại bằng account wiener:peter. Khi này Burpsuite sẽ bắt được GET /my-account?id=wiener cũng với cookie khi đăng nhập.

![alt text](images/image-45.png)

Quay trở lại sửa lại cookie và username thành cookie khi đăng nhập acc wiener và username:wiener và send.

![alt text](images/image-46.png)

Lúc đấy account wiener sẽ được upgrade quyền admin và hoàn thành bài lab

![alt text](images/image-47.png)


# __Lab: Referer-based access control__

Access Lab, sử dụng account admin để đăng nhập và nâng cấp quyền hạn cho account carlos

![alt text](images/image-48.png)

Sử dụng Burpsuite để bắt được GET /admin-roles, Send to Repeater.Đăng xuất khỏi account admin và vào lại bằng account wiener:peter. Khi này Burpsuite sẽ bắt được GET /my-account?id=wiener cũng với cookie khi đăng nhập.

![alt text](images/image-49.png)

Quay trở lại sửa lại cookie và username thành cookie khi đăng nhập acc wiener và username:wiener và Send.

![alt text](images/image-50.png)

Lúc đấy account wiener sẽ được upgrade quyền admin và hoàn thành bài lab

![alt text](images/image-51.png)