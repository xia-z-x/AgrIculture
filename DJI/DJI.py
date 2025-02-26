from djitellopy import Tello
import os
import sys
import cv2
import time
sys.path.append(os.path.abspath('./weather'))
from weather import get_weather

# 连接无人机
try:
    Tello.connect()
    battery = str(Tello.get_battery())
except Exception as e:  # 捕获所有异常
    print ("飞行器连接失败，请检查WIFI连接。")
    os._exit(1)

#起飞条件判断
try:
    weather_info = get_weather()  # 获取天气信息
    weather_description = weather_info['description']
    weather_wind = weather_info['wind_speed']
except Exception as e:  # 捕获所有异常
    weather_info =  "获取天气失败，请检查连接"
    weather_description = weather_info
    weather_wind = weather_info

if weather_description != str("晴") or str("阴") :
    print ("当前天气不适宜巡飞，任务取消。")
    os._exit(0)
if weather_wind > 5.5 : #m/s
    print ("当前风力不适宜巡飞，任务取消。")
    os._exit(0)
if battery < 80 :
    print ("飞行器电量低于80%，任务取消。")
    os._exit(0)

# 主任务
class FarmSurvey:
    def __init__(self, drone, config_path="./config/fly_info.txt", altitude=100, output_dir="./Cache/DJI/"):
        self.drone = drone
        self.config_path = config_path
        self.altitude = altitude
        self.output_dir = output_dir
        self.flight_path = []

        # 创建保存目录
        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)

    def load_coordinates(self):
        """
        从配置文件加载坐标
        """
        if not os.path.exists(self.config_path):
            raise FileNotFoundError(f"配置文件 {self.config_path} 不存在！")
        
        with open(self.config_path, 'r') as f:
            lines = f.readlines()
            # 假设每个点格式为 "x,y" (以厘米为单位)
            self.flight_path = [tuple(map(int, line.strip().split(','))) for line in lines]

    def take_photo(self, file_name):
        """
        拍照并保存图片
        :param file_name: 图片文件名
        """
        print(f"Taking photo and saving as {file_name}...")
        frame_read = self.drone.get_frame_read()
        cv2.imwrite(file_name, frame_read.frame)
        time.sleep(2)

    def execute_mission(self):
        """
        执行飞行任务
        """
        print("Connecting to drone...")
        self.drone.connect()

        print("Starting video stream...")
        self.drone.streamon()

        # 起飞到指定高度
        print("Taking off...")
        self.drone.takeoff()
        time.sleep(2)

        print(f"Moving up to altitude of {self.altitude} cm...")
        self.drone.move_up(self.altitude)

        # 加载选点坐标
        print("Loading flight path...")
        self.load_coordinates()

        # 执行飞行任务
        for i, (x, y) in enumerate(self.flight_path):
            print(f"Flying to point {i + 1}: (x={x} cm, y={y} cm)")
            
            # 移动到目标点
            # 如果 x 和 y 是相对距离 (以厘米为单位)，使用 move_xxx 方法
            if x > 0:
                self.drone.move_forward(x)
            elif x < 0:
                self.drone.move_back(-x)

            if y > 0:
                self.drone.move_right(y)
            elif y < 0:
                self.drone.move_left(-y)

            time.sleep(2)  # 模拟飞行时间

            # 拍照
            file_name = os.path.join(self.output_dir, f"photo_{i + 1}.png")
            self.take_photo(file_name)

        # 返回起飞点
        print("Returning to start point...")
        start_point = self.flight_path[0]
        if start_point[0] > 0:
            self.drone.move_back(start_point[0])
        elif start_point[0] < 0:
            self.drone.move_forward(-start_point[0])

        if start_point[1] > 0:
            self.drone.move_left(start_point[1])
        elif start_point[1] < 0:
            self.drone.move_right(-start_point[1])

        time.sleep(2)

        # 降落
        print("Landing...")
        self.drone.land()
        self.drone.streamoff()
        self.drone.end()


if __name__ == "__main__":
    tello = Tello()
    mission = FarmSurvey(tello)
    mission.execute_mission()