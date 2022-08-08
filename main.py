import botlink
import simuse
import time
from selenium.webdriver import ChromeOptions
import sougou_spider
import messagesend
from selenium import webdriver
from selenium.webdriver import ChromeOptions
import time
import pandas as pd
import mengniang_spider

excel = pd.read_excel('./config.xls', index_col=0, dtype='object')

group = excel['添加的群'].values
adminqq = excel['管理员账号'].values  
key = excel['Http KEY'][0]
host = excel['HOST'][0]
port = excel['PORT'][0]
botqq = excel['BOT QQ'][0]
code = excel['是否使用简略信息'][0]
driver = excel['搜索引擎'][0]
print('当前引擎:', driver)
print('简略模式:', code)
key = dict(verifyKey=key)


# 连接bot
session, host = botlink.linkbot(key=key, host=host, port=port, botqq=botqq)
print('启用该功能的群:', group)

# 打开浏览器, 准备截图
options = ChromeOptions()
options.add_argument('--disable-software-rasterizer')
options.add_argument('-ignore-certificate-errors')
options.add_argument('--headless')
options.add_argument('--disable-gpu')
options.add_argument('--no-sandbox')

web = webdriver.Chrome(options=options)
web.get('https://baike.sogou.com/')

# 开始监听会话
while True:
    msg = simuse.Fetch_Message(host=host, session=session, deal=1)
    if msg == 0:
        continue
    try:
        g = msg[0]['group']
        sender = msg[0]['sender']
        msg = msg[0]['messagechain'][1]['text']
        
        if str(g) not in str(group):
            continue
        if '百科 ' in msg:

            keyword = msg.replace('百科 ', '')
            if driver == '搜狗百科':
                if code == '是':
                    messagesend.sendmessage_txt(group=g, session=session, message='简略模式搜索中....', host=host)
                    img = sougou_spider.search_less(web=web, word=keyword)
                    if img == 0:
                        messagesend.sendmessage_txt(group=g, session=session, message='搜索出错，该词条未收录', host=host)
                        continue
                    print('发送图片中..')
                    t1 = time.time()
                    messagesend.sendmessage_img(group=g, session=session, message=img, host=host)
                    t2 = time.time()
                    print('发送用时', t2-t1,'s')
                else:
                    messagesend.sendmessage_txt(group=g, session=session, message='详细模式搜索中....等待时间可能较长', host=host)
                    img = sougou_spider.search_more(web=web, word=keyword)
                    if img == 0:
                        messagesend.sendmessage_txt(group=g, session=session, message='搜索出错，该词条未收录', host=host)
                        continue
                    
                    print('发送图片中..')
                    t1 = time.time()
                    messagesend.sendmessage_img(group=g, session=session, message=img, host=host)
                    t2 = time.time()
                    print('发送用时', t2-t1,'s')
            if driver == '萌娘百科':
                if code == '是':
                    messagesend.sendmessage_txt(group=g, session=session, message='简略模式搜索中....', host=host)
                    img = mengniang_spider.search_less(web=web, word=keyword)
                    if img == 0:
                        messagesend.sendmessage_txt(group=g, session=session, message='搜索出错，该词条未收录', host=host)
                        continue
                    print('发送图片中..')
                    messagesend.sendmessage_img(group=g, session=session, message=img, host=host)
                else:
                    messagesend.sendmessage_txt(group=g, session=session, message='详细模式搜索中....等待时间可能较长', host=host)
                    img = mengniang_spider.search_more(web=web, word=keyword)
                    if img == 0:
                        messagesend.sendmessage_txt(group=g, session=session, message='搜索出错，该词条未收录', host=host)
                        continue
                    print('发送图片中..')
                    messagesend.sendmessage_img(group=g, session=session, message=img, host=host)



        
        
        elif '/切换模式' in msg:
            if sender in adminqq:
                if code == '是':
                    code = '否'
                    messagesend.sendmessage_txt(group=g, session=session, message='切换成功，当前为详细搜索', host=host)
                else:
                    code = '是'
                    messagesend.sendmessage_txt(group=g, session=session, message='切换成功，当前为简略搜索', host=host)
            else:
                messagesend.sendmessage_txt(group=g, session=session, message='只有管理员可以切换模式', host=host)

        elif '/切换引擎' in msg:
            if sender in adminqq:
                if driver == '搜狗百科':
                    driver = '萌娘百科'
                    messagesend.sendmessage_txt(group=g, session=session, message='当前引擎切换为萌娘百科', host=host)
                elif driver == '萌娘百科':
                    driver = '搜狗百科'
                    messagesend.sendmessage_txt(group=g, session=session, message='当前引擎切换为搜狗百科', host=host)
                    web.get('https://baike.sogou.com/')
            
            else:
                messagesend.sendmessage_txt(group=g, session=session, message='只有管理员可以切换引擎', host=host)




            
    except:
        continue
        
        
    
    time.sleep(1)
    
    

    
