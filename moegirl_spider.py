import time
from urllib.parse import urlencode, quote_plus

import requests
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

USER_AGENT = "Mozilla/5.0 (X11; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/109.0"
REQUEST_HEADER = requests.utils.default_headers()
MOEGIRL_API = "https://zh.moegirl.org.cn/api.php"
SEARCH_PAYLOAD = {
    "action": "opensearch",
    "format": "json",
    "formatversion": 2,
    "namespace": 0,
    "limit": 10
}

REQUEST_HEADER.update(
    {
        'User-Agent': USER_AGENT,
        "Referer": "https://zh.moegirl.org.cn/",
        "X-Requested-With": "XMLHttpRequest",
        "Origin": "https://zh.moegirl.org.cn",
        "Accept": "application/json, text/javascript, */*; q=0.01"
    }
)


def search_less(web, word):
    try:
        web.set_page_load_timeout(5)

        find_wiki(web, word, True)
        find_announce(web)

        WebDriverWait(web, 20).until(EC.presence_of_element_located((By.ID, 'mw-body')))
        print("Find mw-body!")
        element = web.find_element(By.ID, 'mw-body')
        web.set_window_size(1920, 1080)
        img = element.screenshot_as_base64
        js = '''
                document.getElementById('mw-body').remove() '''

        web.execute_script(js)
        web.set_page_load_timeout(10)
        return img
    except Exception as e:
        print('发生了一个错误: ' + str(e))
        web.set_page_load_timeout(10)
        return 0


def search_more(web, word):
    try:
        web.set_page_load_timeout(12)

        find_wiki(web, word, True)
        find_announce(web)

        WebDriverWait(web, 20).until(EC.presence_of_element_located((By.ID, 'mw-body')))
        print("Find mw-body!")
        element = web.find_element(By.ID, 'mw-body')
        if element.size['height'] > 8000:
            web.set_window_size(element.size['width'], 8000)
        else:
            web.set_window_size(element.size['width'], element.size['height'])
        img = element.screenshot_as_base64
        js = '''
                document.getElementById('mw-body').remove() '''

        web.execute_script(js)
        web.set_page_load_timeout(10)
        return img
    except Exception as e:
        print('发生了一个错误: ' + str(e))
        web.set_page_load_timeout(10)
        return 0


def find_announce(web):
    try:
        if web.find_element(By.CSS_SELECTOR, ".n-card"):
            print("发现公告")
            web.find_element(By.XPATH, '/html/body/div[2]/div/div/div[1]/div/div[3]/div[1]/button').click()
            time.sleep(0.6)
    except:
        pass


def find_wiki(web, word, ignoreTimeout=False):
    search_result = requests.get(MOEGIRL_API + get_search_payload(word), headers=REQUEST_HEADER).json()
    try:
        web.get(str(search_result[3][0]))
    except TimeoutException as e:
        if not ignoreTimeout:
            raise e


def get_search_payload(word):
    _search_payload = SEARCH_PAYLOAD
    _search_payload["search"] = word
    return "?"+urlencode(_search_payload, quote_via=quote_plus)
