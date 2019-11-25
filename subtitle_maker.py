# -*- coding: utf-8 -*-
# @Time    : 19-8-16 上午9:53
# @Author  : Redtree
# @File    : subtitle_maker.py
# @Desc :

import os
from aip import AipSpeech
import nltk
from urllib import request, parse
import json
import random

def reset_wav(old_path,new_path):
    try:
       res = os.system('ffmpeg -y -i '+old_path+' -ar 16000 -ac 1 '+new_path)
       if res==0:
           return 'success'
       else:
           return 'error'
    except Exception as err:
        print('音频转换失败:'+str(err))
        return 'error'


def mp4_to_wav(mp4_path,wav_path):

    try:
       res = os.system('ffmpeg -i '+mp4_path+' -f wav -ar 16000 -ac 1 '+wav_path)
       if res==0:
           return 'success'
       else:
           return 'error'
    except Exception as err:
        print('音频提取失败:'+str(err))
        return 'error'

# 读取文件
def get_file_content(filePath):
    with open(filePath, 'rb') as fp:
        return fp.read()

def speech2text(filepath, cuid='yixue', dev_pid=1737, rate=16000, format='wav'):
    # 识别本地文件
    try:
        APP_ID = '16590304'
        API_KEY = 'itxU5q7d5OnYEWk2pPibv18U'
        SECRET_KEY = '37aGi2oPfh5WZ9whYhXGAUi7i3YmjkeN'
        client = AipSpeech(APP_ID, API_KEY, SECRET_KEY)
        res = client.asr(get_file_content(filepath), format, rate, {
            'dev_pid': dev_pid,
            'cuid': cuid,
        })
        text = 'error'
        rtext = ''
        if res['err_no'] == 0:
            text = res['result']
            for t in text:
                rtext = rtext + t
        else:
            return text

        return rtext
    except Exception as err:
        print('ASR识别异常:'+str(err))
        return 'error'


def cutSentence(input):  # 结巴分词
    res = nltk.word_tokenize(input)  # 默认是精确模式
    return res


#获取音频时长
def get_time_long(file_path):
    try:
       CMD1 = 'ffmpeg -i '+file_path
       CMD2 = ''' 2>&1 | grep 'Duration' | cut -d ' ' -f 4 | sed s/,//'''
       res = os.popen(CMD1+CMD2)
       x = res.read()
       return x

    except Exception as err:
        print('音频转换失败:'+str(err))
        return 'error'


def youdao_auto_translator(input_text):
    try:
        req_url = 'http://fanyi.youdao.com/translate'  # 创建连接接口
        # 创建要提交的数据
        Form_Date = {}
        Form_Date['i'] = input_text  # 要翻译的内容可以更改
        Form_Date['doctype'] = 'json'

        data = parse.urlencode(Form_Date).encode('utf-8')  # 数据转换
        response = request.urlopen(req_url, data)  # 提交数据并解析
        html = response.read().decode('utf-8')  # 服务器返回结果读取
        # print(html)
        # 可以看出html是一个json格式
        translate_results = json.loads(html)  # 以json格式载入
        translate_results = translate_results['translateResult'][0][0]['tgt']  # json格式调取

        if str(translate_results).strip(' ') == "":
            return ''
        return translate_results
    except Exception as err:
        return ''

def dojob():

    mp4_to_wav('test.mp4','test.wav')
    r = speech2text('test.wav')
    #print(r)
    # a = get_time_long('test.wav')
    # print(a)
    # b = str(a).split(':')[-1]
    # print(b)
    #r = '''there's just some cultural things that people need to get used to they don't smile unless they're around people they love and they're genuinely happy any other smile is considered being fake and actually really admire that I think we probably smiled through much you're in Americaand so they don't really smile and photographs at all ever some of the youth maybe are getting there now but even if it's a really happy day even wedding days sometimes it just doesyeah that's how it'''
    rl = cutSentence(r)

    n=0
    cur = ''
    for l in rl:
        cur = cur +  ' '+ l
        n+=1
        if n >9:
            print(cur)
            cur = ''
            n=0

    print('翻译:')
    fr = youdao_auto_translator(r)
    frl = fr.split(',')
    for f in frl:
        print(f)

dojob()