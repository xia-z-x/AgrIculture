from djitellopy import Tello

def main():
    # 创建 Tello 对象
    tello = Tello()

    try:
        # 连接无人机
        tello.connect()
        print(f"connect,battery：{tello.get_battery()}%")

       

    except Exception as e:
        print(f"err：{e}")

    finally:
        # 断开连接
        tello.end()
        print("disc")

if __name__ == "__main__":
    main()