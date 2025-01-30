import os
import shutil
import subprocess

# 创建临时文件夹
os.makedirs('runtime', exist_ok=True)




# 删除临时文件
shutil.rmtree('runtime')

# 创建Web
subprocess.run(["python", "./UI/web.py"])
