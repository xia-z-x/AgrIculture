# AgrIculture
Powered by [QDU](https://www.qdu.edu.cn/)❤️

> **智慧农业的温暖实践：用无人机、人工智能图像识别和大语言模型助力现代农业发展。**

---

## 项目简介 📖

AgrIculture是一项聚焦智慧农业的创新实践项目。我们通过整合无人机采集技术、人工智能图像识别、大语言模型以及实时天气数据，构建了一套高效、智能的农田管理解决方案。项目的核心目标是帮助农民减少冬季巡田次数，优化耕作方式，提高农业生产效率，并减轻劳动负担，为打造现代化农业生态贡献技术力量。  

---

## 项目背景 🌍

农业是人类生存与发展的根基，但传统农业方式在冬季面临着诸多难题：  
- 农民需要在寒冷的天气里频繁巡田，耗时费力且效率低下。  
- 作物生长状况的判断依赖经验，缺乏科学依据，容易造成资源浪费。  
- 农田管理难以实现精细化，病虫害防治、土壤改良等关键环节往往滞后。  

随着人工智能和无人机技术的快速发展，智慧农业成为破解这些难题的希望所在。本项目旨在通过技术与农业深度结合，为农民提供便捷、精准的农田管理工具，让科技不仅高效，更有温度。  

---

## 项目特色 ✨

### 🎯 **核心功能**  
1. **无人机采集农田图像**：通过高分辨率图像和多光谱传感器，精确记录作物生长情况。  
2. **人工智能图像分析**：快速识别作物叶片颜色、茎叶形态、病害特征等关键信息。  
3. **实时天气数据整合**：结合温度、湿度、降水等环境因素，进行多维度农田评估。  
4. **大语言模型生成建议**：智能生成针对性的耕作方案，包括施肥、灌溉、防治病害等具体指导。  

### 🛠 **技术亮点**  
- **无人机技术**：实现田间覆盖面广、采集效率高的地块监测。  
- **图像识别与分析**：利用深度学习模型，精准检测作物生长状态及潜在问题。  
- **大语言模型**：结合农业知识库与实时数据，生成人性化、科学化的耕作建议。  
- **数据驱动农业**：通过多源数据的融合分析，让农业逐步迈向智能化、数据化、科学化。  

### 🌱 **项目目标**  
- 减少农民冬季巡田的次数，减轻劳动强度。  
- 提供精准的耕作建议，提升农业管理效率。  
- 推动智慧农业技术的落地，助力农业现代化发展。  

---

## 项目架构 🛠  

```
📂 AgrIculture
├── 📂 config              # 用户配置文件
├── 📂 DJI                 # 无人机图像采集与处理模块
├── 📂 image-analysis      # 图像识别与病害检测模块
├── 📂 weather             # 天气数据获取与整合模块
├── 📂 language-model      # 大语言模型建议生成模块
├── 📂 UI                 #用户界面
├── 📂 TTS                #语音播报
├── 📂 Cache              #缓存文件
├── main.py                #主程序
├── requirements.txt       #项目依赖
└── README.md              # 项目说明文档
```

---

## 安装与运行 🔧  

### 1️⃣ 克隆项目代码  
```bash
git clone https://github.com/xia-z-x/AgrIculture.git
cd AgrIculture
```

### 2️⃣ 填写API
从  https://api.openweathermap.org/  获取API并写入  ./config/weather_api_key.txt

### 3️⃣ 安装依赖  
确保计算机已安装 Python 3.12 及以上版本，运行以下命令安装项目依赖：  
```bash
pip install -r requirements.txt
```

### 4️⃣ 连接到飞行器
将电脑连接到Tello飞行器的WIFI.

### 5️⃣ 运行node.js服务  
确保计算机已安装 node.js ，运行以下命令启动node.js服务：  
```bash
node ./DJI/server.js
```

### 6️⃣ 启动项目  
运行以下命令启动主程序：  
```bash
python ./main.py
```

### 特别说明   
**本项目虽然会在起飞前进行必要的安全检测，但请在起飞前亲自确认飞行环境安全，并做好随时接管飞行器的准备！！！**
若发生安全隐患，本项目**概不负责**
主程序启动后会立即执行一次巡飞（若条件合适），并会在此后的每天8点进行巡飞并更新内容。

---

## TODO 🌟  

在现有功能的基础上，我们计划进一步优化与扩展：  
[ ] 1. **实现农害具体分析**：为加快开发进度，目前仅支持使用简单的颜色检测规则大致分析农害，后续将替换为深度学习模型。  
[ ] 2. **自动规划飞行线路**：由手动规划飞行线路转为选择巡查区域后自动规划线路。  
[ ] 3. **添加支持机型**：由于目前其他非行业级的DJI机型并无已存在的电脑直接控制方案，故仅及于Tello开发，但Tello性能过低，必然无法满足大规模巡查的需求，因此后续将尝试电脑连接RC遥控器对飞行器进行控制。  
[ ] 4. **修改天气获取调用API**  

---

## 参与贡献 🤝  

欢迎对智慧农业感兴趣的开发者、农学研究者与农业从业者参与到本项目中！  
如有任何建议或意见，请提交 Issue 或 Pull Request，我们会及时处理。  

---

## 联系我们 📩  

- **GitHub**：[@xia-z-x](https://github.com/xia-z-x)  

---

## 特别鸣谢 🙏  

[QDU](https://www.qdu.edu.cn/)、[ChatGPT](https://chatgpt.com/)、[Bootstrap](https://icons.bootcss.com/)

感谢所有支持本项目的团队成员、农业专家以及对智慧农业充满热情的伙伴们！  
让我们共同努力，用科技与温情助力农业发展，让田间不再孤单！  

---

**田野不孤，爱与智慧同行。** 🌾❤️
