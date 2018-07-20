import wave
import pyaudio
from datetime import datetime


CHUNK = 1024  # 缓存块的大小
FORMAT = pyaudio.paInt16  # 取样值的量化格式
RATE = 8000   # 取样频率，百度语音识别库指定8000
CHANNELS = 1  # 声道数，百度语音识别库指定1
RECORD_SECONDS = 5  # 时间段，秒

def record_wave(to_dir=None):
    if to_dir is None:
        to_dir = "./"

    pa = pyaudio.PyAudio()
    
    # format 取样值的量化格式
    # channels 声道数
    # rate 取样频率，一秒内对声音信号的采集次数
    # input 输入流标志
    # frames_per_buffer 底层缓存块的大小
    stream = pa.open(format = FORMAT,
                     channels = CHANNELS,
                     rate = RATE,
                     input = True,
                     frames_per_buffer = CHUNK)

    print("* recording")

    # 
    save_buffer = []
    for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
        audio_data = stream.read(CHUNK)
        save_buffer.append(audio_data)

    print("* done recording")

    # stop
    stream.stop_stream()
    stream.close()
    pa.terminate()

    # wav path
    file_name = datetime.now().strftime("%Y-%m-%d_%H_%M_%S")+".wav"
    if to_dir.endswith('/'):
        file_path = to_dir + file_name
    else:
        file_path = to_dir + "/" + file_name

    # save file
    wf = wave.open(file_path, 'wb')
    wf.setnchannels(CHANNELS)
    wf.setsampwidth(pa.get_sample_size(FORMAT))
    wf.setframerate(RATE)
    
    # 注意join 前的类型，如果是str类型会出错
    wf.writeframes(b''.join(save_buffer))
    wf.close()

    return file_path

