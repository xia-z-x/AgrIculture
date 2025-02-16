import os
import shutil
import subprocess
import logging
from multiprocessing import Process
from time import sleep

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
        os.makedirs('runtime', exist_ok=True)
        logging.info("创建临时目录 'runtime'.")
        
        # 开始飞行操作（记录至/runtime）
        #run_subprocess(["python", "./DJI/DJI.py"])

        # 图像分析（覆盖记录至./result.txt）
        #run_subprocess(["python", "./image-analysis/image-analysis.py"])
        
        # TTS
        #run_subprocess(["python", "./TTS/TTS.py"])
        
        # 清理临时文件
        #shutil.rmtree('runtime')
        logging.info("临时目录 'runtime' 已删除.")

        # 生成建议（覆盖记录至./result.txt）
        #run_subprocess(["python", "./language-model/language-model.py"])

    except Exception as e:
        logging.error(f"发生意外错误: {e}")

    # 结束Web界面线程
    #sleep (7200)
    sleep (10)
    web_thread.terminate()
    web_thread.join()
    
if __name__ == "__main__":
    # 22点后拒绝执行，防止bug(todo)
    
    main()
    # 0点清除所有result内容(todo)
    print("1")
    sleep(1)
    main()#test pass!!!!!!
    # 0点刷新Web页面并即刻结束进程(todo)
    
    # 下一个8点重新启动(todo)
    