import os
import cv2
import numpy as np

def analyze_image(image_path):
    try:
        # 读取图片
        image = cv2.imread(image_path)
        if image is None:
            return f"{os.path.basename(image_path)}: 无法读取图片"
        
        # 转换为 HSV 颜色空间
        hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
        
        # 定义农害或生长不良的简单检测规则
        lower_yellow = np.array([20, 100, 100])  # 黄色下界
        upper_yellow = np.array([30, 255, 255])  # 黄色上界

        lower_brown = np.array([10, 50, 50])  # 褐色下界
        upper_brown = np.array([20, 150, 150])  # 褐色上界

        # 检测黄色和褐色区域
        yellow_mask = cv2.inRange(hsv, lower_yellow, upper_yellow)
        brown_mask = cv2.inRange(hsv, lower_brown, upper_brown)

        # 计算区域面积
        yellow_area = np.sum(yellow_mask > 0)
        brown_area = np.sum(brown_mask > 0)
        total_area = image.shape[0] * image.shape[1]

        # 判断比例阈值
        yellow_ratio = yellow_area / total_area
        brown_ratio = brown_area / total_area

        # 如果黄色或褐色区域超过一定比例，判定为农害或生长不良
        if yellow_ratio > 0.05:  # 5% 黄色
            return f"{os.path.basename(image_path)}: 检测到疑似农害 (黄色区域占比 {yellow_ratio:.2%})"
        elif brown_ratio > 0.05:  # 5% 褐色
            return f"{os.path.basename(image_path)}: 检测到生长不良 (褐色区域占比 {brown_ratio:.2%})"
        else:
            return f"{os.path.basename(image_path)}: 生长良好"
    except Exception as e:
        return f"{os.path.basename(image_path)}: 分析失败，错误信息: {str(e)}"

def analyze_images_in_directory(directory, output_file):
    results = []
    if not os.path.exists(directory):
        print(f"目录 {directory} 不存在！")
        return

    # 获取目录中的所有图片文件
    image_files = [f for f in os.listdir(directory) if f.lower().endswith(('.png', '.jpg', '.jpeg'))]
    if not image_files:
        print(f"目录 {directory} 中没有图片文件！")
        return

    # 分析每张图片
    for image_file in image_files:
        image_path = os.path.join(directory, image_file)
        result = analyze_image(image_path)
        results.append(result)
        print(result)  # 打印结果以便调试

    # 将结果写入文件
    with open(output_file, 'w', encoding='utf-8') as f:
        for line in results:
            f.write(line + '\n')
    print(f"分析结果已写入 {output_file}")

if __name__ == "__main__":
    image_directory = "./Cache/DJI/"
    output_file = "./Cache/image_analysis_result.txt"
    analyze_images_in_directory(image_directory, output_file)