from djitellopy import tello
# 连接无人机
tello.connect()
#基础飞行动作

#起飞条件判断
battery = str(tello.get_battery())
#weather = 
#wind = 


#获取设置路线（点模式：每个点储存位置信息及下一步动作）
