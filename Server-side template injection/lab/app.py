from flask import Flask, request, render_template_string

app = Flask(__name__)

# Giao diện HTML mẫu
BASE_TEMPLATE = """
<!DOCTYPE html>
<html lang="vi">
<head>
    <meta charset="UTF-8">
    <title>SSTI Demo Lab</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 40px; background-color: #f4f4f9; }
        .container { max-width: 600px; margin: auto; background: white; padding: 20px; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); }
        .alert { padding: 15px; background-color: #ffdddd; border-left: 6px solid #f44336; margin-bottom: 20px; }
        .product { border: 1px solid #ddd; padding: 15px; border-radius: 4px; }
        .btn { display: inline-block; padding: 8px 12px; background: #007bff; color: white; text-decoration: none; border-radius: 4px; margin-top: 10px; }
    </style>
</head>
<body>
    <div class="container">
        <h2>Cửa hàng Demo SSTI</h2>
        
        {% if message %}
        <div class="alert">
            <strong>Thông báo:</strong> """ + "{USER_INPUT}" + """
        </div>
        {% endif %}

        <div class="product">
            <h3>Sản phẩm: Áo thun Hacker</h3>
            <p>Giá: 250.000 VNĐ</p>
            <p>Tình trạng: <strong>Hết hàng</strong></p>
            <a href="/?message=Rất tiếc, sản phẩm này hiện đã hết hàng!" class="btn">Kiểm tra tồn kho</a>
        </div>
    </div>
</body>
</html>
"""

@app.route('/')
def index():
    # Lấy tham số 'message' từ URL
    user_message = request.args.get('message', '')
    
    # LỖ HỔNG Ở ĐÂY: Nối trực tiếp input của người dùng vào chuỗi template trước khi render
    vulnerable_template = BASE_TEMPLATE.replace("{USER_INPUT}", user_message)
    
    return render_template_string(vulnerable_template, message=bool(user_message))

if __name__ == '__main__':
    # Chạy server ở chế độ debug trên cổng 5000
    app.run(host='127.0.0.1', port=5000, debug=True)