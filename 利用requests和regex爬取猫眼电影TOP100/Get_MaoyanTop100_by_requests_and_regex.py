# -*- coding: utf-8 -*-
"""
Created on Tue Jun 26 11:35:42 2018

@author: Nicobuss

爬取的相关信息有：电影名次、电影名称、主演、上映时间、评分

 pattern = re.compile('.*?board-index-.*?">(.*?)</i>.*?class="name">.*?'
                         + '"boarditem-click".*?"{movieId:.*?}">+(.*?)</a>.*?class="star">'
                         + '(.*?)</p>.*?class="releasetime">(.*?)</p>.*?<p class="score">'
                         + '<i class="integer">(.*?)</i><i class="fraction">(.*?)</i></p>', re.S)

"""

import re
import time
import requests
from multiprocessing import Pool
import json
from http.cookiejar import CookieJar
from requests.exceptions import RequestException

s = requests.Session()
s.cookies = CookieJar()

header = {
    'user-agent': 'Baiduspider+',
}

def getHTML(url, code='utf-8'):
    try:
        response = s.get(url, headers=header)
        response.raise_for_status()
        response.encoding = code
        return response.text
    except RequestException:
        print('getHTML Error')


def parseHTML(html):
    pattern = re.compile('.*?board-index-.*?">(.*?)</i>.*?class="name">.*?'
                         + '"boarditem-click".*?"{movieId:.*?}">+(.*?)</a>.*?class="star">'
                         + '(.*?)</p>.*?class="releasetime">(.*?)</p>.*?<p class="score">'
                         + '<i class="integer">(.*?)</i><i class="fraction">(.*?)</i></p>', re.S)

    items = re.findall(pattern, str(html))      #需要把html字符串化，否则报错：TypeError: expected string or bytes-like object

    for item in items:
        yield {
            '序号': item[0],
            '电影名': item[1],
            '主演': item[2].strip(),
            '上映时间': item[3],
            '评分': item[4] + item[5],
        }

def writePAGE(content):
    with open('result.txt', 'a' ) as f:
        f.write(str(content) + '\n')
        #f.write(json.dumps(content , ensure_ascii=False) + '\n')
        f.close()


def main(page):
    url = 'https://maoyan.com/board/4?offset=' + str(page)
    html = getHTML(url)
    items = parseHTML(html)

    for item in items:
        print(item)
        writePAGE(item)


if __name__ == '__main__':
    start = time.time()

    pool = Pool()
    pool.map(main, [page * 10 for page in range(10)])
    pool.close()  # 关闭进程池，不接受新的进程
    pool.join()  # 主进程阻塞等待子进程的退出

    end = time.time()
    print('It spends %s s' % (end - start))
