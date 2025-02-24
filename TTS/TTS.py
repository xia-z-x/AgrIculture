#实现运行后从/language-model/result.txt中读取内容并生成mp3文件放于/TTS/TTS.mp3
import os
import logging
import pyttsx3

# 设置日志配置
logging.basicConfig(level=logging.INFO)

def text_to_speech(text,output_path):
    try:
        # 如果目标文件已存在，先删除
        if os.path.exists(output_path):
            os.remove(output_path)
            logging.info(f"已删除已存在的文件: {output_path}")
            
        # 初始化pyttsx3引擎
        engine = pyttsx3.init()

        # 可选：设置属性如语速、音量等
        rate = engine.getProperty('rate')   # 获取当前语速
        engine.setProperty('rate', rate-50)  # 减慢语速

        volume = engine.getProperty('volume')  # 获取当前音量
        engine.setProperty('volume', volume+0.25)  # 提高音量

        # 设置语音为中文（根据系统支持的语言包）
        voices = engine.getProperty('voices')
        chinese_voice_found = False
        for voice in voices:
            if "zh" in str(voice.languages):  # 简单地通过languages属性判断是否为中文发音
                engine.setProperty('voice', voice.id)
                chinese_voice_found = True
                break

        if not chinese_voice_found:
            logging.warning("未找到支持中文的语音包，将使用默认语音。")

        # 将文本转换为语音并播放
        #engine.say(text)
        #engine.runAndWait()
    #except Exception as e:
        #logging.error(f"Text to speech conversion failed: {e}")
        # 保存文本为 MP3 文件
        engine.save_to_file(text, output_path)
        engine.runAndWait()
        logging.info(f"语音文件已保存到: {output_path}")
    except Exception as e:
        logging.error(f"Text-to-speech conversion failed: {e}")
        
def play_text_as_speech(file_path):
    try:
        # 使用UTF-8编码打开并读取文本文件内容
        with open(file_path, 'r', encoding='utf-8') as file:
            text = file.read()
        
        # 转换文本到语音
        text_to_speech(text,output_path)
    except FileNotFoundError:
        logging.error(f"无法找到文件: {file_path}, 请检查文件名或路径是否正确。")
    except UnicodeDecodeError:
        logging.error(f"文件 {file_path} 的编码可能不是UTF-8，请确认文件编码后重试。")
    except Exception as e:
        logging.error(f"An error occurred: {e}")

def main():
    # 固定文件路径
    file_path = "./Cache/language_model_result.txt"#将文件路径改为想要打开的文件
    output_path = "./Cache/TTS_result.mp3"
    # 直接播放文本作为语音
    play_text_as_speech(file_path)

if __name__ == "__main__":
    main()
