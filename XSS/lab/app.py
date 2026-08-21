from flask import Flask, request

app = Flask(__name__)

# 1. Trang chủ hiện thanh tìm kiếm
@app.route('/')
def trang_chu():
    return '''
        <h2>Trang web tìm kiếm siêu cấp</h2>
        <form action="/tim-kiem" method="GET">
            <input type="text" name="q" placeholder="Nhập từ khóa vào đây..." size="40">
            <button type="submit">Tìm kiếm</button>
        </form>
    '''

# 2. Trang xử lý kết quả (Bị lỗi Reflected XSS)
@app.route('/tim-kiem')
def tim_kiem():
    tu_khoa = request.args.get('q', '')
    
    # Nối thẳng biến người dùng nhập vào HTML mà không thèm Encode
    giao_dien_html = f'''
        <h2>Kết quả tìm kiếm:</h2>
        <p>Bạn vừa tìm chữ: {tu_khoa}</p>
        <br>
        <a href="/">Quay lại trang chủ</a>
    '''
    return giao_dien_html

if __name__ == '__main__':
    app.run(port=5000)