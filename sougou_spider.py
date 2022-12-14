from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver import ChromeOptions

def search_more(web, word):
    
    web.find_element(By.XPATH, '//*[@id="searchText"]').clear()
    web.find_element(By.XPATH, '//*[@id="searchText"]').send_keys(word)
    web.find_element(By.XPATH, '//*[@id="enterLemma"]').click()
    try:
        element = WebDriverWait(web, 5).until(EC.presence_of_element_located((By.CLASS_NAME, 'lemma_container')))
        element = web.find_element(By.CLASS_NAME, 'lemma_container')
        if element.size['height'] > 8000:
            web.set_window_size(element.size['width'], 8000)
        else:
            web.set_window_size(element.size['width'], element.size['height'])
        img = web.find_element(By.CLASS_NAME, 'lemma_container').screenshot_as_base64
        js = '''
                document.getElementsByClassName('lemma_container')[0].remove() '''
        
        web.execute_script(js)
        return img
    except:
        web.get('https://baike.sogou.com/')
        return 0
    

def search_less(web, word):
    try:
        web.find_element(By.XPATH, '//*[@id="searchText"]').clear()
        web.find_element(By.XPATH, '//*[@id="searchText"]').send_keys(word)
        web.find_element(By.XPATH, '//*[@id="enterLemma"]').click()
        element = WebDriverWait(web, 5).until(EC.presence_of_element_located((By.CLASS_NAME, 'lemma_container')))
        element = web.find_element(By.CLASS_NAME, 'lemma_container')
        
        web.set_window_size(element.size['width'], element.size['height'])
        img = web.find_element(By.CLASS_NAME, 'abstract_wrap').screenshot_as_base64
        js = '''
                document.getElementsByClassName('lemma_container')[0].remove() '''
        
        web.execute_script(js)
        return img
    except:
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
        search_more(web=web, word=input('??????????????????'))

