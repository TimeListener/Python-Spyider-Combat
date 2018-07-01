# 此爬虫适合爬取利用Ajax加载的页面

import requests
import urllib.parse
from requests.exceptions import RequestException
import json
import re
from bs4 import BeautifulSoup
from json.decoder import JSONDecodeError
import os
from hashlib import md5
from multiprocessing import Pool

#此库为了在Pool()中引入多参数，本次用不上
#from pathos.multiprocessing import ProcessingPool as Pool

#定义一个头部
header = {
    'user-agent': "Baiduspider+"
}

# 获取索引页的html
def get_one_index(offset, keyword, code='utf-8'):
    data = {
        'offset': offset,
        'format': 'json',
        'keyword': keyword,
        'autoload': 'true',
        'count': '20',
        'cur_tab': 1
    }
    # urlencode函数可将字符串以URL编码，用于编码处理，返回字符串
    url = 'https://www.toutiao.com/search_content/' + '?' + urllib.parse.urlencode(data)

    try:
        r = requests.get(url, headers=header)
        r.raise_for_status()
        r.encoding = 'utf-8'
        # 返回的是json
        return r.text
    except RequestException:
        print('get_one_index 出现错误')
        return None


# 解析索引页的html文件，提取出图片的url地址（注意迭代输出）
def parse_one_html(html):
    try:
        # 将已编码的 JSON 字符串解码为 Python 对象
        html = json.loads(html)
        # 判断html是否有"data"这个键
        if html and 'data' in html.keys():
            for item in html.get('data'):
                yield item.get("article_url")
    except JSONDecodeError:
        pass

# 获取在parse_one_html()函数中获取的url的html
def get_page_html(url):
    try:
        r = requests.get(url, headers=header)
        if r.status_code == 200:
            return r.text
        return None
    except RequestException:
        print('get_one_index 出现错误', url)
        return None

# 解析get_page_html()函数中的html里的图片地址
def parse_html_by_1(html):
    soup = BeautifulSoup(html, 'lxml')
    title = soup.select('title')[0].get_text()
    if title:
        print(title)
    #使用正则表达式得到图片的url(此处获取的url需要处理)
    image_pattern = re.compile('gallery: JSON.parse\("(.*?)"\)', re.S)
    image_content = re.search(image_pattern, html)

    #如果页面的图片是滑动切换的，且用regex可以得到url的话：
    if image_content:
        data = json.loads(image_content.group(1).replace('\\', ''))
        if data:
            if data and 'sub_images' in data.keys():
                sub_images = data.get('sub_images')
                images = [item.get('url') for item in sub_images]
                for image in images:
                    get_image_html(image)
    #如果页面的图片是滑屏查看的，则需要换一种正则公式，即parse_html_by_2
    else:
        parse_html_by_2(html)

#如果图片页面是滑屏查看的，则使用一下的方法
def parse_html_by_2(html):
    pattern = re.compile('src&#x3D;&quot;(.*?)&quot;',re.S)
    images =re.findall(pattern,html)
    for image in images:
        print(image)
        get_image_html(image)

#下载图片至本地的"F://photos"文件夹中
def get_image_html(url):
    print('\r 开始下载:%s'%url,end='')
    r = requests.get(url)
    if r.status_code == 200:
        write_image(r.content)
    return None

#文件的写入
def write_image(content):
    file_path = '{0}/{1}.{2}'.format('f://photos/', md5(content).hexdigest(), 'jpg')
    if not os.path.exists(file_path):
        with open(file_path, 'wb') as f:
            f.write(content)
            f.close()


def main(i):
    index_html = get_one_index(i*20, '模特')
    for item in parse_one_html(index_html):
        if item:
            page_html = get_page_html(item)
            parse_html_by_1(page_html)


if __name__ == "__main__":
    #使用多进程爬取
    pool = Pool()

    page = int(input('请输入页数：'))
    offset = [i for i in range(page+1)]
    pool.map(main,offset)

    pool.close()
    pool.join()
