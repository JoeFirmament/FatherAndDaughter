#!/usr/bin/python
# -*- coding: UTF-8 -*-
import urllib.parse
import urllib.request
from turtle import *
from time import sleep

#这是python3，原先py2里的urllib2或者其他都包含在了py3的urllib里了，
# py3里的urllib里的parse和request一定要这么导入，直接import urllib
# 是不行的
 
import time
import json
import hashlib
import base64
import record

 

my_text   = "爸爸"



def go_to(x, y):
   up()
   goto(x, y)
   down()


def big_Circle(size):  #函数用于绘制心的大圆
   speed(10)
   for i in range(150):
       forward(size)
       right(0.3)

def small_Circle(size):  #函数用于绘制心的小圆
   speed(10)
   for i in range(210):
       forward(size)
       right(0.786)

def line(size):
   speed(1)
   forward(51*size)

def heart( x, y, size):
   go_to(x, y)
   left(150)
   begin_fill()
   line(size)
   big_Circle(size)
   small_Circle(size)
   left(120)
   small_Circle(size)
   big_Circle(size)
   line(size)
   end_fill()

def arrow():
   pensize(10)
   setheading(0)
   go_to(-400, 0)
   left(15)
   forward(150)
   go_to(339, 178)
   forward(150)

def arrowHead():
   pensize(1)
   speed(5)
   color('red', 'red')
   begin_fill()
   left(120)
   forward(20)
   right(150)
   forward(35)
   right(120)
   forward(35)
   right(150)
   forward(20)
   end_fill()

def main():
    global my_text
    file_path = record.record_wave()
    f = open(file_path, 'rb')
    #rb表示以二进制格式只读打开文件
 
    file_content = f.read()
    #file_content 是二进制内容，bytes类型
    #由于Python的字符串类型是str，在内存中以Unicode表示，一个字符对应若干个字节。
    # 如果要在网络上传输，或者保存到磁盘上，就需要把str变为以字节为单位的bytes
    # 以Unicode表示的str通过encode()方法可以编码为指定的bytes，例如：
    # >> > 'ABC'.encode('ascii')
    # b'ABC'
    # >> > '中文'.encode('utf-8')
    # b'\xe4\xb8\xad\xe6\x96\x87'
    # >> > '中文'.encode('ascii')
    # Traceback(most
    # recent
    # call
    # last):
    # File
    # "<stdin>", line 1, in < module >
    # UnicodeEncodeError: 'ascii' codec can't encode characters in position 0-1: ordinal not in range(128)
 
    base64_audio = base64.b64encode(file_content)
    #base64.b64encode()参数是bytes类型，返回也是bytes类型
 
    body = urllib.parse.urlencode({'audio': base64_audio})
    url = 'https://api.xfyun.cn/v1/service/v1/iat'
    api_key = '77f0d5177778807794e1b15230e9b7e5' #api key在这里
    x_appid = '5b51692e'  # appid在这里
    param = {"engine_type": "sms8k", "aue": "raw"}
 
    x_time = int(int(round(time.time() * 1000)) / 1000)
 
    x_param = base64.b64encode(json.dumps(param).replace(' ', '').encode('utf-8'))
    # 这是3.x的用法，因为3.x中字符都为unicode编码，而b64encode函数的参数为byte类型，
    # 所以必须先转码为utf-8的bytes
 
    # >> print(x_param)
    # >> b'YWJjcjM0cjM0NHI ='
    # 结果和我们预想的有点区别，我们只想要获得YWJjcjM0cjM0NHI =，而字符串被b
    # ''包围了。这时肯定有人说了，用正则取出来就好了。。。别急。b表示
    # byte的意思，我们只要再将byte转换回去就好了:
    # >> x_param = str(x_param, 'utf-8')
 
    # Python3 字符编码 https://www.cnblogs.com/284628487a/p/5584714.html
 
    x_checksum_content = api_key + str(x_time) + str(x_param, 'utf-8')
    x_checksum = hashlib.md5(x_checksum_content.encode('utf-8')).hexdigest()
    # python3里的hashlib.md5()参数也是要求bytes类型的，x_checksum_content是以Unicode
    # 编码的，所以需要转成bytes。
    # 讯飞api说明：
    # 授权认证，调用接口需要将Appid，CurTime, Param和CheckSum信息放在HTTP请求头中；
    # 接口统一为UTF-8编码；
    # 接口支持http和https；
    # 请求方式为POST。
 
    x_header = {'X-Appid': x_appid,
                'X-CurTime': x_time,
                'X-Param': x_param,
                'X-CheckSum': x_checksum}
 
    req = urllib.request.Request(url = url, data = body.encode('utf-8'), headers = x_header, method = 'POST')
    #不要忘记url = ??, data = ??, headers = ??, method = ?? 中的“ = ”，这是python3！！
 
    result = urllib.request.urlopen(req)
    result = json.loads(result.read().decode('utf-8'))

    #result = result.read().decode('utf-8')
    #返回的数据需要再以utf-8解码
    if result["code"] == "0":
        my_text = result["data"]
        pensize(10)
        color('red', 'pink')
        #getscreen().tracer(30, 0) #取消注释后，快速显示图案
        heart(-300, 0, 1)          #画出第一颗心，前面两个参数控制心的位置，函数最后一个参数可控制心的大小
        setheading(0)             #使画笔的方向朝向x轴正方向
        #heart(-80, -100, 1.5)     #画出第二颗心
        #arrow()                   #画出穿过两颗心的直线
        #arrowHead()               #画出箭的箭头
        go_to(0, 0)
        pensize(1)
        write("你说了:\""+my_text+"\" ,爸爸也爱你", move=True, align="left", font=("微软雅黑", 20, "normal"))
        done()
  
    #print(result)
    return
 
if __name__ == '__main__':
    main()
 
