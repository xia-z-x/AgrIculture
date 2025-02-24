from ast import Import
import os
from pickle import TRUE
import shutil
import subprocess
import logging
from multiprocessing import Process
from time import sleep
import sys
from datetime import datetime,timedelta
import time

from _pytest.legacypath import Cache

# 设置日志记录
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def run_subprocess(command):
    """运行子进程并记录日志"""
    try:
        subprocess.run(command, check=True)
        logging.info(f"命令 '{' '.join(command)}' 执行完成.")
    except subprocess.CalledProcessError as e:
        logging.error(f"运行命令 '{' '.join(command)}' 时发生错误: {e}")

def start_web_ui():
    """启动Web界面"""
    run_subprocess(["python", "./UI/web.py"])

def main():
    

    # 启动Web界面线程
    web_thread = Process(target=start_web_ui)
    web_thread.start()

    try:
        # 创建临时目录
        os.makedirs('./Cache/DJI', exist_ok=True)
        logging.info("创建临时目录 'DJI'.")
        
        # 开始飞行操作（记录至/runtime）
        run_subprocess(["python", "./DJI/DJI.py"])

        # 图像分析（覆盖记录至./result.txt）
        run_subprocess(["python", "./image-analysis/image-analysis.py"])
        
        # 清理临时文件
        shutil.rmtree('./Cache/DJI')
        logging.info("临时目录 'DJI' 已删除.")

        # 生成建议（覆盖记录至./result.txt）
        run_subprocess(["python", "./language-model/language-model.py"])
        
        # TTS
        run_subprocess(["python", "./TTS/TTS.py"])

    except Exception as e:
        logging.error(f"发生意外错误: {e}")

    # 结束Web界面线程
    #sleep (7200)
    sleep (10)
    web_thread.terminate()
    web_thread.join()
    
while TRUE:
    current_time = datetime.now()
    if current_time.hour >= 23:
        sys.exit("检测到23时后运行，为避免巡飞过程包含0时导致次日缓存溢出，程序已强制退出。")
    else:
        main()
        
        # 0点清除所有result内容（含TTS）（将大语言改为“今日尚未巡飞。”）(todo)
        # 0点秒更新+刷新Web页面并即刻结束进程(todo)
        now = datetime.now()
        # 计算下一个午夜的时间
        next_midnight = (now + timedelta(days=1)).replace(hour=0, minute=0, second=0, microsecond=0)
        # 计算休眠时间（秒）
        sleep_seconds = (next_midnight - now).total_seconds()
        # 计算小时、分钟和秒
        hours, remainder = divmod(sleep_seconds, 3600)
        minutes, seconds = divmod(remainder, 60)
        print(f"程序将在 {int(hours)} 小时 {int(minutes)} 分 {int(seconds)} 秒后清除当日记录。")
        time.sleep(sleep_seconds)
        if os.path.exists("./Cache/image_analysis_result.txt"):
            os.remove("./Cache/image_analysis_result.txt")
            with open("./Cache/image_analysis_result.txt", 'w') as file:
                pass
        if os.path.exists("./Cache/language_model_result.txt"):
            os.remove("./Cache/language_model_result.txt")
            with open("./Cache/language_model_result.txt", 'w') as file:
                file.write("今日尚未巡飞。")
        print ("当日记录已清除。")
        # 下一个8点重新启动(todo)
        next_eight_am = now.replace(hour=8, minute=0, second=0, microsecond=0)
        # 如果当前时间已经超过 8 点，则设置为次日的 8 点
        if now >= next_eight_am:
            next_eight_am += timedelta(days=1)
        # 计算休眠时间（秒）
        sleep_seconds = (next_eight_am - now).total_seconds()
        # 计算小时、分钟和秒
        hours, remainder = divmod(sleep_seconds, 3600)
        minutes, seconds = divmod(remainder, 60)
        print(f"程序将在 {int(hours)} 小时 {int(minutes)} 分 {int(seconds)} 秒（次日8时）后再次运行。")
        time.sleep(sleep_seconds)
        
    
    