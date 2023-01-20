from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait


def search_less(web, word):
    try:
        web.set_page_load_timeout(5)
        try:
            web.get('https://zh.moegirl.org.cn/' + word)
        except TimeoutException:
            pass
        if web.find_element(By.CSS_SELECTOR, ".n-card"):
            web.find_element(By.XPATH, '/html/body/div[2]/div/div/div[1]/div/div[3]/div[3]/div/button').click()
            print("关闭公告")
        element = WebDriverWait(web, 20).until(EC.presence_of_element_located((By.ID, 'mw-body')))
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
        print('发生了一个错误: '+str(e))
        web.set_page_load_timeout(10)
        return 0


def search_more(web, word):
    try:
        web.set_page_load_timeout(5)
        try:
            web.get('https://zh.moegirl.org.cn/' + word)
        except TimeoutException:
            pass
        if web.find_element(By.CSS_SELECTOR, ".n-card"):
            web.find_element(By.XPATH, '/html/body/div[2]/div/div/div[1]/div/div[3]/div[3]/div/button').click()
            print("关闭公告")
        element = WebDriverWait(web, 20).until(EC.presence_of_element_located((By.ID, 'mw-body')))
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
        print('发生了一个错误: '+str(e))
        web.set_page_load_timeout(10)
        return 0
