import requests

def read_api_key(file_path):
    """从指定路径的文件中读取API密钥"""
    try:
        with open(file_path, 'r') as file:
            api_key = file.read().strip() # 使用strip()去除可能存在的多余空格和换行符
        return api_key
    except FileNotFoundError:
        print(f"无法找到文件: {file_path}")
        return None
    except Exception as e:
        print(f"读取API密钥时出错: {e}")
        return None

def get_location():
    """获取当前位置信息"""
    try:
        response = requests.get('http://ip-api.com/json/?lang=zh-CN')
        location_data = response.json()
        if response.status_code == 200 and location_data['status'] == 'success':
            return {
                'city': location_data['city'],
                'lat': location_data['lat'],
                'lon': location_data['lon']
            }#将位置信息传回到主程序
        else:
            return None
    except Exception as e:
        print(f"无法获取位置信息: {e}")
        return None

def get_weather(api_key, lat, lon):
    """根据经纬度获取天气信息"""
    base_url = "https://api.openweathermap.org/data/2.5/weather"
    params = {
        'lat': lat,
        'lon': lon,
        'appid': api_key,
        'units': 'metric',
        'lang': 'zh_cn'
    }
    try:
        response = requests.get(base_url, params=params)
        weather_data = response.json()
        
        if response.status_code == 200:
            weather = {
                'description': weather_data['weather'][0]['description'],
                'temperature': weather_data['main']['temp'],
                'wind_speed': weather_data['wind']['speed'], # 风速
                'wind_direction': weather_data['wind'].get('deg', '未知'), # 风向，可能不存在
            }#将天气信息传回到主程序
            return weather
        else:
            return "无法获取天气信息"
    except Exception as e:
        print(f"获取天气信息时出错: {e}")
        return None

# 使用方法：
if __name__ == "__main__":
    file_path = 'C:\\Users\\gongpiqi\\Desktop\\API\\api_key.txt' # 确保使用双反斜杠或原始字符串处理Windows路径
    #将file_path替换为真正的路径
    api_key = read_api_key(file_path)
    if api_key:
        location = get_location()
        if location:
            weather_info = get_weather(api_key, location['lat'], location['lon'])
            if weather_info and isinstance(weather_info, dict):
                print(f"城市: {location['city']}, 天气: {weather_info['description']}, 温度: {weather_info['temperature']}°C, 风速: {weather_info['wind_speed']}m/s, 风向: {weather_info['wind_direction']}°")
            else:
                print(weather_info) # 输出错误信息
        else:
            print("无法确定您的位置")
