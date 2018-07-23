from pyquery import PyQuery as pq
from proxypool.get_html import getHTML
import re

ip_list = []

class GetIp(object):

    def __init__(self):
        self.Crawl_66ip()
        self.Crawl_ip181()
        self.Crawl_ip3366()
        self.Crawl_89ip()
        self.Crawl_xroxy()
        self.Crawl_kuaidaili()
        self.Crawl_xicidaili()
        self.Crawl_kxdaili()
        # self.Crawl_premproxy()
        self.return_list()

    # 爬取 http://www.66ip.cn/2.html 代理
    def Crawl_66ip(self):
        for page in range(1, 5):
            url = 'http://www.66ip.cn/{}.html'.format(page)
            html = getHTML(url)
            if html:
                doc = pq(html)
                items = doc('.containerbox table tr:gt(0)').items()
                for item in items:
                    ip = item.find('td:nth-child(1)').text()
                    port = item.find('td:nth-child(2)').text()
                    ip_list.append(':'.join([ip, port]))

    # 爬取http://www.ip181.com/
    def Crawl_ip181(self):
        start_url = 'http://www.ip181.com/'
        html = getHTML(start_url)
        if html:
            ip_address = re.compile('<tr.*?>\s*<td>(.*?)</td>\s*<td>(.*?)</td>')
            # \s* 匹配空格，起到换行作用
            re_ip_address = ip_address.findall(html)
            for address, port in re_ip_address:
                result = address + ':' + port
                ip_list.append(result.replace(' ', ''))


    def Crawl_ip3366(self):
        for page in range(1, 4):
            start_url = 'http://www.ip3366.net/free/?stype=1&page={}'.format(page)
            html = getHTML(start_url)
            if html:
                ip_address = re.compile('<tr>\s*<td>(.*?)</td>\s*<td>(.*?)</td>')
                # \s * 匹配空格，起到换行作用
                re_ip_address = ip_address.findall(html)
                for address, port in re_ip_address:
                    result = address + ':' + port
                    ip_list.append(result.replace(' ', ''))

    def Crawl_kxdaili(self):
        for i in range(1, 5):
            start_url = 'http://www.kxdaili.com/ipList/{}.html#ip'.format(i)
            html = getHTML(start_url)
            if html:
                ip_address = re.compile('<tr.*?>\s*<td>(.*?)</td>\s*<td>(.*?)</td>')
                # \s* 匹配空格，起到换行作用
                re_ip_address = ip_address.findall(html)
                for address, port in re_ip_address:
                    result = address + ':' + port
                    ip_list.append(result.replace(' ', ''))

    # def Crawl_premproxy(self):
    #     for i in ['China-01', 'China-02', 'China-03', 'China-04', 'Taiwan-01']:
    #         start_url = 'https://premproxy.com/proxy-by-country/{}.htm'.format(i)
    #         html = getHTML(start_url)
    #         if html:
    #             ip_address = re.compile('<td data-label="IP:port ">(.*?)</td>')
    #             re_ip_address = ip_address.findall(html)
    #             for address_port in re_ip_address:
    #                 ip_list.append(address_port.replace(' ', ''))

    def Crawl_xroxy(self):
        for i in ['CN', 'TW']:
            start_url = 'http://www.xroxy.com/proxylist.php?country={}'.format(i)
            html = getHTML(start_url)
            if html:
                ip_address1 = re.compile("title='View this Proxy details'>\s*(.*).*")
                re_ip_address1 = ip_address1.findall(html)
                ip_address2 = re.compile("title='Select proxies with port number .*'>(.*)</a>")
                re_ip_address2 = ip_address2.findall(html)
                for address, port in zip(re_ip_address1, re_ip_address2):
                    address_port = address + ':' + port
                    ip_list.append(address_port.replace(' ', ''))

    def Crawl_kuaidaili(self):
        for i in range(1, 4):
            start_url = 'http://www.kuaidaili.com/free/inha/{}/'.format(i)
            html = getHTML(start_url)
            if html:
                ip_address = re.compile('<td data-title="IP">(.*?)</td>')
                re_ip_address = ip_address.findall(html)
                port = re.compile('<td data-title="PORT">(.*?)</td>')
                re_port = port.findall(html)
                for address, port in zip(re_ip_address, re_port):
                    address_port = address + ':' + port
                    ip_list.append(address_port.replace(' ', ''))

    def Crawl_xicidaili(self):
        for i in range(1, 3):
            start_url = 'http://www.xicidaili.com/nn/{}'.format(i)
            headers = {
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
                'Cookie': '_free_proxy_session=BAh7B0kiD3Nlc3Npb25faWQGOgZFVEkiJWZlYjQ0NTQwYWJhZDk4MzAwMjg5ZTk2OWQ4MTRjMzNjBjsAVEkiEF9jc3JmX3Rva2VuBjsARkkiMUJJNXpoNmE4d291SlFoOU14TXM1cktJZUFwSlduaWlxSHErWTkzZ29tUTQ9BjsARg%3D%3D--d53869b3c6a6ceef0720cbd349689ccc1f90773d; Hm_lvt_0cf76c77469e965d2957f0553e6ecf59=1532240670; Hm_lpvt_0cf76c77469e965d2957f0553e6ecf59=1532240670',
                'Host': 'www.xicidaili.com',
                'Referer': 'http://www.xicidaili.com/nn/3',
                'Upgrade-Insecure-Requests': '1',
            }
            html = getHTML(start_url, headers=headers)
            if html:
                find_trs = re.compile('<tr class.*?>(.*?)</tr>', re.S)
                trs = find_trs.findall(html)
                for tr in trs:
                    find_ip = re.compile('<td>(\d+\.\d+\.\d+\.\d+)</td>')
                    re_ip_address = find_ip.findall(tr)
                    find_port = re.compile('<td>(\d+)</td>')
                    re_port = find_port.findall(tr)
                    for address, port in zip(re_ip_address, re_port):
                        address_port = address + ':' + port
                        ip_list.append(address_port)

    def Crawl_89ip(self):
        start_url = 'http://www.89ip.cn/apijk/?&tqsl=1000&sxa=&sxb=&tta=&ports=&ktip=&cf=1'
        html = getHTML(start_url)
        if html:
            find_ips = re.compile('(\d+\.\d+\.\d+\.\d+:\d+)', re.S)
            ip_ports = find_ips.findall(html)
            for address_port in ip_ports:
                ip_list.append(address_port)

    def return_list(self):
        return ip_list


