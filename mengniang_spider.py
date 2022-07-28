
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver import ChromeOptions
import warnings




def search_less(web, word):
    try:
        warnings.simplefilter('ignore', ResourceWarning)
        web.get('https://zh.moegirl.org.cn/'+word)
        WebDriverWait(web, 10).until(EC.presence_of_element_located((By.ID, 'mw-body')))
        element = web.find_element(By.ID, 'mw-body')
        web.set_window_size(1920, 1080)
        img = element.screenshot_as_base64
        js = '''
                document.getElementById('mw-body').remove() '''
        
        web.execute_script(js)
        return img
    except:
        return 0

def search_more(web, word):
    try:
        web.get('https://zh.moegirl.org.cn/'+word)
        WebDriverWait(web, 10).until(EC.presence_of_element_located((By.ID, 'mw-body')))
        element = web.find_element(By.ID, 'mw-body')
        web.set_window_size(element.size['width'], element.size['height'])
        img = element.screenshot_as_base64
        js = '''
                document.getElementById('mw-body').remove() '''
        
        web.execute_script(js)
        return img
    except:
        return 0
    

if __name__ == "__main__":
    options = ChromeOptions()
    options.add_argument('--disable-software-rasterizer')
    options.add_argument('-ignore-certificate-errors')
    options.add_argument('--headless')
    options.add_argument('--disable-gpu')
    web = webdriver.Chrome(options=options)
    search_less(web=web, word='栗山未来')

