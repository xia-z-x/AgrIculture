import os
import datetime
import sys
import torch
from transformers import AutoModelForCausalLM, AutoTokenizer
import accelerate

# 添加路径到自定义模块
sys.path.append(os.path.abspath('./weather'))
from weather import get_weather, get_location


def check_device():
    """检查 GPU 是否可用，并返回设备"""
    if torch.cuda.is_available():
        return torch.device("cuda")
    else:
        print("警告：CUDA 不可用，切换到 CPU 模式运行（性能较低）")
        return torch.device("cpu")


def load_model_and_tokenizer(model_path, device):
    """加载模型和分词器"""
    try:
        # 加载分词器
        tokenizer = AutoTokenizer.from_pretrained(model_path)
        # 加载模型并手动指定设备
        model = AutoModelForCausalLM.from_pretrained(
            model_path,
            torch_dtype=torch.float16 if device.type == "cuda" else torch.float32,  # 根据设备选择精度
            device_map="auto",
            low_cpu_mem_usage=True
        ).to(device)  # 手动将模型加载到设备上
        return model, tokenizer
    except Exception as e:
        print(f"模型加载失败：{e}")
        sys.exit(1)


def chat_with_model(model, tokenizer, user_input, device, max_length=1000):
    """与模型交互生成回复"""
    try:
        # 将输入转为张量并移动到指定设备
        inputs = tokenizer.encode(
            user_input + tokenizer.eos_token,
            return_tensors='pt'
        ).to(device)

        # 使用 torch.no_grad() 避免显存消耗
        with torch.no_grad():
            outputs = model.generate(
                inputs,
                max_length=max_length,
                pad_token_id=tokenizer.eos_token_id
            )
        # 解码生成的回复
        response = tokenizer.decode(outputs[:, inputs.shape[-1]:][0], skip_special_tokens=True)
        return response
    except torch.cuda.OutOfMemoryError:
        print("显存不足，尝试减少输入长度或使用更小的模型！")
        torch.cuda.empty_cache()  # 清理显存
        sys.exit(1)
    except Exception as e:
        print(f"生成回复失败：{e}")
        return "模型生成失败，请检查输入或模型文件！"


def main():
    # 检查设备
    device = check_device()

    # 模型路径
    model_path = "huihui-ai/DeepSeek-R1-Distill-Qwen-7B-abliterated"

    # 加载模型和分词器
    model, tokenizer = load_model_and_tokenizer(model_path, device)

    # 获取当前日期
    current_date = datetime.datetime.now().strftime("%Y 年%m 月%d 日")

    # 获取位置信息和天气信息
    try:
        location = get_location()
    except Exception as e:
        print(f"获取位置信息失败：{e}")
        location = "暂时无法获取"

    try:
        weather_info = get_weather()
        weather_view = weather_info['description']
    except Exception as e:
        print(f"获取天气信息失败：{e}")
        weather_view = "暂时无法获取"

    # 从文件读取巡查结果
    try:
        with open("./Cache/image_analysis_result.txt", "r", encoding="utf-8") as file:
            image_analysis_result = file.read().strip()
    except FileNotFoundError:
        print("巡查结果文件未找到，使用默认提示")
        image_analysis_result = "巡查结果文件未找到。"

    # 构造用户输入
    user_input = f"""
    假设你是一名农业专家，你所在的位置是{location}，今天是{current_date}，天气{weather_view}，
    无人机巡查结果显示{image_analysis_result}，
    请你据此写出作物现状和耕作建议，各写成一段话简要说明。
    """

    # 调用模型生成回复
    try:
        response = chat_with_model(model, tokenizer, user_input, device)
    except Exception as e:
        print(f"模型生成失败：{e}")
        response = "大语言模型错误，请检查日志！"

    # 保存模型回复到文件
    file_path = "./Cache/language_model_result.txt"
    try:
        with open(file_path, "w", encoding="utf-8") as file:
            file.write(response)
        print(f"模型回复已保存到文件：{file_path}")
    except Exception as e:
        print(f"保存回复失败：{e}")


if __name__ == "__main__":
    main()