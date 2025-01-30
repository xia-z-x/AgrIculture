import http.server
import socketserver
import webbrowser
import os
import sys

sys.path.append(os.path.abspath('./weather'))
sys.path.append(os.path.abspath('./language-model'))

from weather import get_weather
from language_model import main

#print("当前工作目录:", os.getcwd())

# 读取用户配置端口
def read_port_from_file(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8-sig') as file:
            return int(file.read().strip())
    except Exception as e:
        print(f"读取端口时出错: {e}.  使用默认端口5678")
        return 5678  # 默认端口

# HTML 内容
weather_info = get_weather()  # 获取天气信息
language_text = main()  # 获取一段话

html_content = f"""
<!DOCTYPE html>
<html lang="zh">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>欢迎使用AgrIculture智慧农业系统</title>
    <style>
        body {{
            font-family: Arial, sans-serif;
            margin: 0;
            padding: 0;
            display: flex;
            flex-direction: column;
            height: 100vh;
        }}
        .header {{
            flex: 1;
            display: flex;
            justify-content: center;
            align-items: center;
            position: relative;
        }}
        .time {{
            font-size: 4em;  /* 放大时间 */
            text-align: center;
        }}
        .weather {{
            position: absolute;
            bottom: 20px;
            right: 20px;
            font-size: 1.5em;  /* 调整天气信息大小 */
        }}
        .footer {{
            flex: 2;  /* 下半部分更大 */
            display: flex;
            justify-content: center;
            align-items: center;
            padding: 20px;
            background-color: #f0f0f0;
        }}
    </style>
</head>
<body>
    <div class="header">
        <div class="time" id="current-time"></div>
        <div class="weather" id="weather-info">{weather_info}</div>
    </div>
    <div class="footer">
        <p>{language_text}</p>
    </div>
    <script>
        function updateTime() {{
            const now = new Date();
            document.getElementById('current-time').textContent = now.toLocaleTimeString();
        }}
        setInterval(updateTime, 1000);
        updateTime();
    </script>
</body>
</html>
"""

# 写入 HTML 文件
with open("index.html", "w", encoding="utf-8") as file:
    file.write(html_content)

# 读取端口
port_file_path = './config/port.txt'
if not os.path.exists(port_file_path):
    print(f"文件不存在: {port_file_path}")
PORT = read_port_from_file(port_file_path)

# 启动 HTTP 服务器
class Handler(http.server.SimpleHTTPRequestHandler):
    def end_headers(self):
        self.send_header('Access-Control-Allow-Origin', '*')
        super().end_headers()

with socketserver.TCPServer(("", PORT), Handler) as httpd:
    print(f"Serving at port {PORT}")
    webbrowser.open(f'http://127.0.0.1:{PORT}/index.html')
    httpd.serve_forever()