# -*- coding: utf-8 -*-
"""
Created on Tue Jun 26 11:35:42 2018

@author: Nicobuss

爬取的相关信息有：电影名次、电影名称、主演、上映时间、评分
"""

import requests
import re

header = {
        'User-Agent':'Baiduspider+'
        }

def getHTML(url,code='utf-8'):
    r = requests.get(url,headers=header)
    if r.status_code == 200:
        r.encoding = code
        return r.text
    else :
        print('getHTML Error')
            
def parsePage(html):
    pattern = re.compile('.*?board-index-.*?">(.*?)</i>.*?class="name">.*?"boarditem-click".*?"{movieId:.*?}">(.*?)</a>.*?class="star">(.*?)</p>.*?class="releasetime">(.*?)</p>.*?<p class="score"><i class="integer">(.*?)</i><i class="fraction">(.*?)</i></p>',re.S)
    content = re.findall(pattern,html)
    return content
        
def main(page):
    url = 'http://maoyan.com/board/4?offset='+str(page)
    html = getHTML(url)
    content = parsePage(html)
    print(content)

if __name__=='__main__':
    for page in range(10):
        main(page*10)
    
    
    