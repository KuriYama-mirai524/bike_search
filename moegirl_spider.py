import warnings

from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait


def search_less(web, word):
    try:
        warnings.simplefilter('ignore', ResourceWarning)
        web.get('https://zh.moegirl.org.cn/' + word)
        print("Start wait...")
        WebDriverWait(web, 20).until(EC.presence_of_element_located((By.ID, 'mw-body')))
        print("Find mw-body!")
        element = web.find_element(By.ID, 'mw-body')
        web.set_window_size(1920, 1080)
        img = element.screenshot_as_base64
        js = '''
                document.getElementById('mw-body').remove() '''

        web.execute_script(js)
        return img
    except Exception as e:
        with open('./printlog.txt', 'a+') as f:
            f.write('发生了一个错误: ' + str(e))
        return 0


def search_more(web, word):
    try:
        web.get('https://zh.moegirl.org.cn/' + word)
        print("Start wait...")
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
        return img
    except Exception as e:
        with open('./printlog.txt', 'a+') as f:
            f.write('发生了一个错误: ' + str(e))
        return 0
