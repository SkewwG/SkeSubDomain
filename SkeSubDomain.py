# 通过爬取主站的链接获取子域
#!/usr/bin/python
# author：ske
# python3
import  requests
import re
import chardet
from optparse import OptionParser
requests.packages.urllib3.disable_warnings()

class getSubDomain:
    def __init__(self, url):
        self.url = url              # 主站
        self.headers = {"User-Agent":"Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.75 Safari/537.36"}
        urlsplit = url.split(".")
        self.domain = url if len(urlsplit) == 2 else urlsplit[-2] + "." + urlsplit[-1]      # 域名
        self.SubDomainList = [url]     # 子域名列表
        # 域名匹配规则
        self.domain_patten = re.compile('https?:\/\/[^"/]+?\.{url}'.format(url=urlsplit[-2] + "\." + urlsplit[-1]))
        # 标题匹配规则
        self.title_patten = re.compile('<title>(.*)?</title>')

    # 开始从主站开始爬取
    def start(self):
        self.getSubDomain(self.url)

    # 获取域名列表
    def getSubDomain(self, url):
        try:
            res = requests.get(url, headers=self.headers, timeout=5, verify=False)  # 作为一个递归查询
            self.code_title(url, res)
            subdomains = list(set(re.findall(self.domain_patten, res.text)))           # 子域名列表,去重结果
            # 遍历匹配到的所有子域名
            for subdomain in subdomains:
                # 如果这个子域名之前没添加进列表里
                if subdomain not in self.SubDomainList:
                    self.SubDomainList.append(subdomain)
                    self.getSubDomain(subdomain)

        except Exception as e:
            pass

    # 获取域名的标题和状态码
    def code_title(self, url, res):
        result = {}
        code = res.status_code
        try:
            cont = res.content
            # 获取网页的编码格式
            charset = chardet.detect(cont)['encoding']
            # 对各种编码情况进行判断
            html_doc = cont.decode(charset)
        except Exception as e:
            html_doc = res.text

        try:
            # self.title_patten = re.compile('<title>(.*)?</title>')
            title = re.search(self.title_patten, html_doc).group(1)
            result['url'],result['code'],result['title'] = url,code,title
        except Exception as e:
            result['url'], result['code'], result['title'] = url, code, 'None'
        finally:
            print(result)
            self.save(str(result))

    def save(self, result):
        with open('{}.txt'.format(self.domain), 'at', encoding='utf-8') as f:
            f.writelines(result+'\n')


if __name__ == "__main__":
    banner = '''
   _____ _  ________        _____       _         _                       _       
  / ____| |/ /  ____|      / ____|     | |       | |                     (_)      
 | (___ | ' /| |__        | (___  _   _| |__   __| | ___  _ __ ___   __ _ _ _ __  
  \___ \|  < |  __|        \___ \| | | | '_ \ / _` |/ _ \| '_ ` _ \ / _` | | '_ \ 
  ____) | . \| |____   _   ____) | |_| | |_) | (_| | (_) | | | | | | (_| | | | | |
 |_____/|_|\_\______| (_) |_____/ \__,_|_.__/ \__,_|\___/|_| |_| |_|\__,_|_|_| |_|
                                                                                  
                                                                                  
                                                                                   '''
    attentionPlz = """
        请输入主站网址，如：http(s)://www.qq.com
    """
    print(banner)
    print(attentionPlz)

    usage = r'usage : %prog python3 getSubDomain.py -u http://www.qq.com'
    parse = OptionParser(usage=usage)
    parse.add_option('-u', '--url', dest='url', type='string', help='url or domain')
    options, args = parse.parse_args()
    getSubDomain(options.url).start()