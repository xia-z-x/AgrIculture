import requests

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
    print("开始聊天！输入'exit'退出程序。")
    while True:
        user_input = input("你: ")
        if user_input.lower() == 'exit':
            break
        response = chat_with_model(user_input)
        print(f"Bot: {response}")
