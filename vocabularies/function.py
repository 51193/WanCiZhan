import urllib.request
import urllib.parse
import json


# 存在问题，然后的内容不仅仅是单词的释义，而且还有其他的引申
def TranslateWord(word):
    # 百度翻译的API接口
    url = "https://fanyi.baidu.com/sug"
    headers = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 '
                  '(KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36'
    }
    # 要加的参数
    data = {
        'kw': word,
    }
    data = urllib.parse.urlencode(data).encode()
    request = urllib.request.Request(url=url, headers=headers, data=data)
    response = urllib.request.urlopen(request).read().decode('unicode_escape')
    # 用Json模块把得到的json数据（其实它就是一种str字符串）转成Python中字典
    response = json.loads(response)['data']
    string = ""
    for word in response:
        string = string + word['k'] + '：' + word['v'] + '\n'
    return string

'''
if __name__ == '__main__':
    word = 'name'
    string = TranslateWord(word)
    print(string)
'''


