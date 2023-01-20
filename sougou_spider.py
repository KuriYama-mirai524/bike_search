from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver import ChromeOptions


def search_more(web, word):
    return search(web, word)


def search_less(web, word):
    return search(web, word, True)


def search(web, word, isLite=False):
    try:
        web.find_element(By.XPATH, '//*[@id="searchText"]').clear()
        web.find_element(By.XPATH, '//*[@id="searchText"]').send_keys(word)
        web.find_element(By.XPATH, '//*[@id="enterLemma"]').click()
        WebDriverWait(web, 5).until(EC.presence_of_element_located((By.CLASS_NAME, 'lemma_container')))
        element = web.find_element(By.CLASS_NAME, 'lemma_container')

        if isLite:
            web.set_window_size(element.size['width'], element.size['height'])
            img = web.find_element(By.CLASS_NAME, 'abstract_wrap').screenshot_as_base64
            web.get('https://baike.sogou.com/')
            return img
        else:
            if element.size['height'] > 8000:
                web.set_window_size(element.size['width'], 8000)
            else:
                web.set_window_size(element.size['width'], element.size['height'])
            img = web.find_element(By.CLASS_NAME, 'lemma_container').screenshot_as_base64
            web.get('https://baike.sogou.com/')
            return img
    except Exception as e:
        print('发生了一个错误: ' + str(e))
        web.get('https://baike.sogou.com/')
        return 0


if __name__ == '__main__':
    options = ChromeOptions()
    options.add_argument('--disable-software-rasterizer')
    options.add_argument('-ignore-certificate-errors')
    options.add_argument('--headless')
    options.add_argument('--disable-gpu')
    web = webdriver.Chrome(options=options)
    web.get('https://baike.sogou.com/')

    for i in range(3):
        search_more(web=web, word=input('输入搜索内容'))
