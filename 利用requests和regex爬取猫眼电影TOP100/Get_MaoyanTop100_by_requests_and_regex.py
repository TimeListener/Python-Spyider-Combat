# -*- coding: utf-8 -*-
"""
Created on Tue Jun 26 11:35:42 2018

@author: Nicobuss

爬取的相关信息有：电影名次、电影名称、主演、上映时间、评分
"""

import requests
import re

#计算下运行时间
import time
#没有使用xxx时，同一网速，用时1.7s

from multiprocessing import Pool
from requests.exceptions import RequestException



header = {
        'User-Agent':'Baiduspider+'
        }

def getHTML(url,code='utf-8'):
    try:
        r = requests.get(url,headers=header)
        if r.status_code == 200:
            r.encoding = code
            return r.text
        else :
            print('getHTML Error')
    except RequestException:
        print('getHTML Error')
            
def parsePage(html):
    pattern = re.compile('.*?board-index-.*?">(.*?)</i>.*?class="name">.*?"boarditem-click".*?"{movieId:.*?}">(.*?)</a>.*?class="star">(.*?)</p>.*?class="releasetime">(.*?)</p>.*?<p class="score"><i class="integer">(.*?)</i><i class="fraction">(.*?)</i></p>',re.S)
    items = re.findall(pattern,html)
    
    for item in items:
        yield {
                'index':item[0],
                'Name':item[1],
                'StarActor':item[2].strip(),
                'ReleaseTime':item[3],
                'Score':item[4]+item[5]
                }
        
def main(page):
    url = 'http://maoyan.com/board/4?offset='+str(page)
    html = getHTML(url)
    items = parsePage(html)
    
    for item in items:
        f.write(item)
    


if __name__=='__main__':
    start = time.time()
    
    f = open('f://result.txt','a')
    
    pool = Pool()
    pool.map(main , [i*10 for i in range(10)])
    pool.close()
    pool.join()
    
    f.close()
    
    end = time.time()
    
    print('It spends %s s'%(end-start))
    
    
    