import os
import shutil
import subprocess
import logging
import threading

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
    web_thread = threading.Thread(target=start_web_ui)
    web_thread.start()

    try:
        # 创建临时目录
        os.makedirs('runtime', exist_ok=True)
        logging.info("创建临时目录 'runtime'.")
        
        # 开始飞行操作
        run_subprocess(["python", "./DJI/DJI.py"])

        # 图像分析
        run_subprocess(["python", "./image-analysis/image-analysis.py"])

        # 清理临时文件
        shutil.rmtree('runtime')
        logging.info("临时目录 'runtime' 已删除.")

        # 生成建议
        run_subprocess(["python", "./language-model/language-model.py"])

    except Exception as e:
        logging.error(f"发生意外错误: {e}")

    # 等待Web界面线程结束
    web_thread.join()

if __name__ == "__main__":
    main()