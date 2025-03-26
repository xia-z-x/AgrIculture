import torch
print(torch.cuda.is_available())  # 应返回 True
print(torch.cuda.device_count())  # 显示可用 GPU 数量
print(torch.cuda.get_device_name(0))  # 显示第一块 GPU 的名称
print(torch.__version__)
import accelerate
print(accelerate.__version__)  # 输出版本号，确保 >= 0.26.0