import requests
import os
import datetime
import sys
sys.path.append(os.path.abspath('./weather'))
from weather import get_weather
from weather import get_location



# 加超时设置
response = requests.get('https://huggingface.co', timeout=30)

print(response.text)
from transformers import AutoModelForCausalLM, AutoTokenizer
import torch

# 加载预训练模型和分词器
model_name = "microsoft/DialoGPT-medium" # 你可以选择其他模型
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForCausalLM.from_pretrained(model_name)

def chat_with_model(user_input):
    # 将输入编码为模型输入格式
    inputs = tokenizer.encode(user_input + tokenizer.eos_token, return_tensors='pt')
    
    # 生成回复
    outputs = model.generate(inputs, max_length=1000, pad_token_id=tokenizer.eos_token_id)
    
    # 解码输出并打印
    response = tokenizer.decode(outputs[:, inputs.shape[-1]:][0], skip_special_tokens=True)
    return response

if __name__ == "__main__":
    #print("开始聊天！输入'exit'退出程序。")
    #while True:
        # 获取当前日期
        current_date = datetime.datetime.now().strftime("%Y 年%m 月%d 日")
        # 位置、天气
        location = get_location()
        try:
            weather_info = get_weather()  # 获取天气信息
            weather_view = (weather_info['description'])
        except Exception as e:  # 捕获所有异常
            weather_info =  "暂时无法获取"
            weather_view = weather_info

        # 从文件读取巡查结果
        try:
            with open("./Cache/image_analysis_result.txt", "r", encoding="utf-8") as file:
                image_analysis_result = file.read().strip()
        except FileNotFoundError:
            image_analysis_result = "巡查结果文件未找到。"

        # 构造响应
        user_input = f"""
        假设你是一名农业专家，你所在的位置是{location}，今天是{current_date}，天气{weather_view}，
        无人机巡查结果显示{image_analysis_result}，
        请你据此写出作物现状和耕作建议，各写成一段话简要说明。
        """        
        #if user_input.lower() == 'exit':
        #    break
        response = chat_with_model(user_input)
        #print(f"Bot: {response}")
        file_path = "./Cache/language_model_result.txt"
    
        # 确保目录存在
        #os.makedirs(os.path.dirname(file_path), exist_ok=True)
    
        # 将 response 内容保存到文件
        with open(file_path, "w", encoding="utf-8") as file:
            file.write(response)
    
        print(f"模型回复已保存到文件：{file_path}")