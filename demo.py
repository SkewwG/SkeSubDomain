import re
a = 'http://xw.qq.com'
ret = re.findall('https?:\/\/[^"/]+?\.qq\.com', a)


import requests
import chardet

urls = ['http://qqgame.qq.com', 'http://service.qq.com', 'http://wx.qq.com', 'http://www.qq.com']

for url in urls:
    print(url)
    res = requests.get(url, verify=False)
    cont = res.content
    # 获取网页的编码格式
    charset = chardet.detect(cont)['encoding']
    print(charset)
    # 对各种编码情况进行判断
    # html_doc = cont.decode('gb2312') if charset == 'GB2312' else res.text
    try:
        html_doc = cont.decode(charset)
    except Exception as e:
        print(e)
        html_doc = res.text
    # if charset == 'GB2312':
    #     html_doc = cont.decode('gb2312')
    # elif charset == 'utf-8':
    #     html_doc = cont.decode('utf-8')
    # elif charset == 'UTF-8-SIG':
    #     html_doc = cont.decode('UTF-8-SIG')
    # else:
    #     html_doc = res.text
    title_patten = '<title>(.*)?</title>'
    titles = re.search(title_patten, html_doc)
    print(titles.group(1))