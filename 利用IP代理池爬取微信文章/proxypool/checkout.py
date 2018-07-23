from urllib3.exceptions import ReadTimeoutError

from proxypool.crawl_ip import GetIp
import requests
from requests.exceptions import ProxyError, ConnectTimeout, ReadTimeout

vaild_ip = []

getip = GetIp()
iplist = getip.return_list()
iplist = list(set(iplist))
print('爬取完毕，开始测试')


class CheckIp(object):

    def __init__(self):
        self.checkout_ip()
        self.return_vaild_ip()

    def checkout_ip(self):
        for ip in iplist:
            try:
                try:
                    try:
                        try:
                            try:
                                try:
                                    try:
                                        print('检测IP中',ip)
                                        proxy = {
                                            'http': ip
                                        }
                                        r = requests.get(url='http://www.baidu.com', proxies=proxy, timeout=5)
                                        if r.status_code == 200:
                                            print(ip, '，此可用~')
                                            vaild_ip.append(ip)
                                        else:
                                            print(ip, ',此代理已作废')
                                    except ConnectionError:
                                        print(ip,'ConnectionError')
                                except ReadTimeout:
                                    print(ip,'ReadTimeout')
                            except ConnectTimeout:
                                print(ip,'连接超时')
                        except ReadTimeoutError:
                            print(ip,'读取超时')
                    except TimeoutError:
                        print(ip,'超时，过了5秒')
                except ProxyError:
                    print(ip, ',此代理已作废')
            except:
                print('未知错误')

    def return_vaild_ip(self):
        return vaild_ip



