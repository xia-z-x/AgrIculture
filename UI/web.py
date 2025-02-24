﻿import http.server
import socketserver
from time import sleep
import webbrowser
import os
import sys

sys.path.append(os.path.abspath('./weather'))
#sys.path.append(os.path.abspath('./language-model'))

from weather import get_weather
#from language_model import main

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
language_text = (lambda file_path: (open(file_path, 'r', encoding='utf-8').read().strip() if os.path.exists(file_path) else "今日尚未巡飞。"))('./Cache/language_model_result.txt')  # 获取建议内容

html_content = f"""
<!DOCTYPE html>
<html lang="zh">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>欢迎使用AgrIculture智慧农业系统</title>
    <style>
        /* 通用样式 */
* {{
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}}
body {{
    font-family: 'Arial', sans-serif;
    color: #333;
    background-color: #ffffff;
    display: flex;
    flex-direction: column;
    height: 100vh;
    overflow: hidden;
}}

/* 头部样式 */
.header {{
    flex: 1;
    display: flex;
    justify-content: center;
    align-items: center;
    position: relative;
    background-color: #f5f5f5;
    border-bottom: 1px solid #ddd;
}}
.time {{
    font-size: 5rem; /* 字体增大 */
    font-weight: bold;
    text-align: center;
    color: #333;
}}
.weather {{
    position: absolute;
    bottom: 20px;
    right: 60px;
    font-size: 2rem; /* 字体增大 */
    font-style: italic;
    color: #555;
}}

/* 图标样式 */
.icon {{
    position: absolute;
    width: 40px;
    height: 40px;
    cursor: pointer;
    fill: #555;
    transition: transform 0.2s ease-in-out, fill 0.2s ease-in-out;
}}
.icon:hover {{
    transform: scale(1.2);
    fill: #388e3c;
}}
.settings-icon {{
    top: 20px;
    right: 20px;
}}
.drone-icon {{
    top: 20px;
    left: 20px;
}}

/* 页脚样式 */
.footer {{
    flex: 1.5;
    display: flex;
    justify-content: center;
    align-items: center;
    padding: 20px;
    background-color: #f9f9f9;
    font-size: 2rem; /* 字体增大 */
    font-weight: 500;
    line-height: 1.5;
    text-align: center;
    color: #444;
    border-top: 1px solid #ddd;
}}

/* 响应式设计 */
@media (max-width: 768px) {{
    .time {{
        font-size: 4rem; /* 小屏幕字体调整 */
    }}
    .weather {{
        font-size: 1.5rem; /* 小屏幕字体调整 */
        right: 20px;
    }}
    .footer {{
        font-size: 1.25rem; /* 小屏幕字体调整 */
        padding: 15px;
    }}
}}
    </style>
</head>
<body>
    <!-- 头部 -->
    <div class="header">
        <div class="time" id="current-time"></div>
        <div class="weather" id="weather-info">{weather_info}</div>
        <!-- 设置图标 -->
        <div class="icon settings-icon" title="设置">
            <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 16 16">
                <path fill-rule="evenodd" d="M11.5 2a1.5 1.5 0 1 0 0 3 1.5 1.5 0 0 0 0-3M9.05 3a2.5 2.5 0 0 1 4.9 0H16v1h-2.05a2.5 2.5 0 0 1-4.9 0H0V3zM4.5 7a1.5 1.5 0 1 0 0 3 1.5 1.5 0 0 0 0-3M2.05 8a2.5 2.5 0 0 1 4.9 0H16v1H6.95a2.5 2.5 0 0 1-4.9 0H0V8zm9.45 4a1.5 1.5 0 1 0 0 3 1.5 1.5 0 0 0 0-3m-2.45 1a2.5 2.5 0 0 1 4.9 0H16v1h-2.05a2.5 2.5 0 0 1-4.9 0H0v-1z"/>
            </svg>
        </div>
        <!-- 无人机图标 -->
        <div class="icon drone-icon" title="无人机">
            <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 16 16">
                <path d="M6.428 1.151C6.708.591 7.213 0 8 0s1.292.592 1.572 1.151C9.861 1.73 10 2.431 10 3v3.691l5.17 2.585a1.5 1.5 0 0 1 .83 1.342V12a.5.5 0 0 1-.582.493l-5.507-.918-.375 2.253 1.318 1.318A.5.5 0 0 1 10.5 16h-5a.5.5 0 0 1-.354-.854l1.319-1.318-.376-2.253-5.507.918A.5.5 0 0 1 0 12v-1.382a1.5 1.5 0 0 1 .83-1.342L6 6.691V3c0-.568.14-1.271.428-1.849m.894.448C7.111 2.02 7 2.569 7 3v4a.5.5 0 0 1-.276.447l-5.448 2.724a.5.5 0 0 0-.276.447v.792l5.418-.903a.5.5 0 0 1 .575.41l.5 3a.5.5 0 0 1-.14.437L6.708 15h2.586l-.647-.646a.5.5 0 0 1-.14-.436l.5-3a.5.5 0 0 1 .576-.411L15 11.41v-.792a.5.5 0 0 0-.276-.447L9.276 7.447A.5.5 0 0 1 9 7V3c0-.432-.11-.979-.322-1.401C8.458 1.159 8.213 1 8 1s-.458.158-.678.599"/>
            </svg>
        </div>
    </div>

    <!-- 页脚 -->
    <div class="footer">
        <p>{language_text}</p>
    </div>

    <script>
        // 更新时间
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