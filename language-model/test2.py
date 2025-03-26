import torch
from transformers import AutoModelForCausalLM, AutoTokenizer

# 模型路径
model_path = "./language-model/models/deepseek-r1-7b"

# 检查 GPU 是否可用
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
assert device.type == "cuda", "CUDA 不可用，无法使用 float16！"

# 加载分词器
tokenizer = AutoTokenizer.from_pretrained(model_path)

# 加载模型并使用 float16
model = AutoModelForCausalLM.from_pretrained(
    model_path,
    torch_dtype=torch.float16
).to(device)

# 编码输入
user_input = "你好，今天的天气怎么样？"
inputs = tokenizer.encode(
    user_input + tokenizer.eos_token,
    return_tensors='pt'
).to(device)

# 生成回复
outputs = model.generate(inputs, max_length=1000, pad_token_id=tokenizer.eos_token_id)

# 解码输出
response = tokenizer.decode(outputs[:, inputs.shape[-1]:][0], skip_special_tokens=True)

print(response)