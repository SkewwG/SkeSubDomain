import re
import requests
# ['https://survey.taobao.com', 'http://zhitongche.taobao.com', 'http://seller-taojinbi.taobao.com', 'https://lovetao.bbs.taobao.com', 'https://i.xue.taobao.com', 'http://shop11669679
# 0.taobao.com', 'http://pics.taobao.com', 'http://jstracker.www.taobao.com']

a = 'https://survey.taobao.com'
#a = 'https://wujin.taobao.com'
res = requests.get(a)
text = res.text
http_pattern = 'https?:\/\/[^/"]*?\.taobao\.com'
http_cmp = re.compile(http_pattern)
urls = re.findall(http_cmp, text)
print(set(urls))
print(len(set(urls)))





# import chardet
#
# urls = ['http://qqgame.qq.com', 'http://service.qq.com', 'http://wx.qq.com', 'http://www.qq.com']
#
# for url in urls:
#     print(url)
#     res = requests.get(url, verify=False)
#     cont = res.content
#     # 获取网页的编码格式
#     charset = chardet.detect(cont)['encoding']
#     print(charset)
#     # 对各种编码情况进行判断
#     # html_doc = cont.decode('gb2312') if charset == 'GB2312' else res.text
#     try:
#         html_doc = cont.decode(charset)
#     except Exception as e:
#         print(e)
#         html_doc = res.text
#     # if charset == 'GB2312':
#     #     html_doc = cont.decode('gb2312')
#     # elif charset == 'utf-8':
#     #     html_doc = cont.decode('utf-8')
#     # elif charset == 'UTF-8-SIG':
#     #     html_doc = cont.decode('UTF-8-SIG')
#     # else:
#     #     html_doc = res.text
#     title_patten = '<title>(.*)?</title>'
#     titles = re.search(title_patten, html_doc)
#     print(titles.group(1))