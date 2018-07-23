import requests
from requests.exceptions import ConnectionError, ReadTimeout


def getHTML(url, **kwargs):
    print('正在请求：' + url)
    try:
        try:
            try:
                r = requests.get(url, timeout=10, **kwargs)
                if r.status_code == 200:
                    r.encoding = 'gb2312'
                    return r.text
                else:
                    print(url, '获取出错，状态码：' + str(r.status_code))
                    return None
            except ReadTimeout:
                print(url,'ReadTimeout')
        except TimeoutError:
            print(url, '请求超时')
    except ConnectionError:
        print(url, '请求失败')
        return None



