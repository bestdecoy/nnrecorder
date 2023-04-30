# 获取虎牙直播的真实流媒体地址。

from contextlib import nullcontext
import requests
import re
import base64
import urllib.parse
import hashlib
import time

def live(e):
    i, b = e.split('?')
    r = i.split('/')
    s = re.sub(r'.(flv|m3u8)', '', r[-1])
    c = b.split('&', 3)
    c = [i for i in c if i != '']
    n = {i.split('=')[0]: i.split('=')[1] for i in c}
    fm = urllib.parse.unquote(n['fm'])
    u = base64.b64decode(fm).decode('utf-8')
    p = u.split('_')[0]
    f = str(int(time.time() * 1e7))
    l = n['wsTime']
    t = '0'
    h = '_'.join([p, t, s, f, l])
    m = hashlib.md5(h.encode('utf-8')).hexdigest()
    y = c[-1]
    url = "{}?wsSecret={}&wsTime={}&u={}&seqid={}&{}".format(i, m, l, t, f, y)
    return url


def get_real_url(room_id):

    # 获取失败或者未开播则为0
    liveTitle = 0
    liveName = 0

    try:
        room_url = 'https://m.huya.com/' + str(room_id)
        header = {
            'Content-Type': 'application/x-www-form-urlencoded',
            'User-Agent': 'Mozilla/5.0 (Linux; Android 5.0; SM-G900P Build/LRX21T) AppleWebKit/537.36 (KHTML, like Gecko) '
                          'Chrome/75.0.3770.100 Mobile Safari/537.36 '
        }
        response = requests.get(url=room_url, headers=header).text
        liveTitle = re.findall(r'"sIntroduction":"([\s\S]*?)",', response)[0].replace(' ', '')
        liveName = re.findall(r'<title>([\s\S]*?)直播', response)[0].replace(' ', '')  # 获取直播间信息
        liveLineUrl = re.findall(r'"liveLineUrl":"([\s\S]*?)",', response)[0]
        liveline = base64.b64decode(liveLineUrl).decode('utf-8')
        if liveline:
            if 'replay' in liveline:
                real_url = 0 # 放录播不录像
                # return '直播录像：' + liveline
            else:
                liveline = live(liveline)
                real_url = ("https:" + liveline).replace("hls", "flv").replace("m3u8", "flv")
                real_url = re.findall(r'^(.*?)&ctype',real_url)[0]
        else:
            real_url = 0 # '未开播或直播间不存在'
    except:
        real_url = 0 # '未开播或直播间不存在'

    return real_url, liveTitle, liveName

if __name__ == '__main__':
    rid = input('输入虎牙直播房间号：\n')
    real_url = get_real_url(rid)
    print('该直播间源地址为：')
    print(real_url)