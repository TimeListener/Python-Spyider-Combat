from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import re
from pyquery import PyQuery as pq
import json

browser = webdriver.Chrome()
wait = WebDriverWait(browser, 10)


def page_regex(content):
    pattern = re.compile('(\d+)')
    pages = re.search(pattern, content).group(1)
    return pages


def search():
    try:
        browser.get('https://www.taobao.com/')
        input = wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR, '#q'))
        )

        submit = wait.until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, '#J_TSearchForm > div.search-button > button'))
        )

        input.clear()
        input.send_keys('美食')
        submit.click()

        total = wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR, '#mainsrp-pager > div > div > div > div.total'))
        ).text

        get_products()

        pages = int(page_regex(total))
        return pages
    except TimeoutException:
        return search()


def next_page(page_number):
    try:
        input = wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR, '#mainsrp-pager > div > div > div > div.form > input'))
        )

        submit = wait.until(
            EC.element_to_be_clickable(
                (By.CSS_SELECTOR, '#mainsrp-pager > div > div > div > div.form > span.btn.J_Submit'))
        )

        input.clear()
        input.send_keys(page_number)
        submit.click()

        get_products()

        wait.until(
            EC.text_to_be_present_in_element(
                (By.CSS_SELECTOR, '#mainsrp-pager > div > div > div > ul > li.item.active > span'), str(page_number))
        )

    except TimeoutException:
        next_page(page_number)


def get_products():
    wait.until(
        EC.presence_of_element_located((By.CSS_SELECTOR, '#mainsrp-itemlist .items .item'))
    )

    html = browser.page_source
    doc = pq(html)
    items = doc('#mainsrp-itemlist .items .item').items()
    for item in items:
        products = {
            'images': item.find('.pic .img').attr('src'),
            'price': item.find('.price').text().replace('\n', ''),
            'number': item.find('.deal-cnt').text()[:-3],
            'location': item.find('.location').text(),
            'shop': item.find('.shop').text(),
            'name': item.find('.title').text().replace('\n', '').replace('\n', '')
        }

        write_content(products)


def write_content(content):
    #  出现illegal multibyte sequence错误，则添加errors = 'ignore'
    with open('f://taobao.txt', 'a', errors='ignore') as f:
        # f.write(str(content))
        f.write(json.dumps(content, ensure_ascii=False) + '\n')
        f.close()


def main():
    pages = search()
    for page in range(2, pages + 1):
        next_page(page)


if __name__ == '__main__':
    main()
