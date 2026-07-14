from flask import Flask, request, send_file
import urllib.parse
import os

app = Flask(__name__)

IMAGE_FOLDER = "images"

@app.route("/")
def home():
    return """
    <!DOCTYPE html>
    <html>
    <head>
        <title>My Blog</title>
    </head>
    <body>

        <h1>My Blog</h1>

        <h3>Article 1</h3>
        <p>Demo Path Traversal Lab</p>

        <img src="/image?filename=trứng_bắc_thảo.jpg" width="400">

    </body>
    </html>
    """

@app.route("/image")
def image():

    filename = request.args.get("filename", "")

    print("=" * 50)
    print("Client gửi :", filename)

    # Developer nghĩ rằng chỉ cần xóa ../ là đủ
    filename = filename.replace("../", "")
    filename = filename.replace("..\\", "")

    print("Sau filter :", filename)

    # ❌ Lỗi: URL decode lần thứ hai
    filename = urllib.parse.unquote(filename)

    print("Sau decode :", filename)

    filepath = os.path.join(IMAGE_FOLDER, filename)

    print("Đường dẫn cuối :", filepath)

    return send_file(filepath)

if __name__ == "__main__":
    app.run(debug=True)