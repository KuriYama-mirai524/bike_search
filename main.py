import time
import traceback

import pandas as pd
from selenium import webdriver
from selenium.webdriver import ChromeOptions

import botlink
import moegirl_spider
import simuse
import sougou_spider
import msg_sender

CONFIG = pd.read_excel('./config.xls', index_col=0, dtype='object')

GROUPS = CONFIG['添加的群'].values
ADMIN_QQ = CONFIG['管理员账号'].values
KEY = CONFIG['Http KEY'][0]
BOT_QQ = CONFIG['BOT QQ'][0]
DRIVER = CONFIG['搜索引擎'][0]
HOST = "http://{}:{}".format(CONFIG['HOST'][0], CONFIG['PORT'][0])

if CONFIG['是否使用简略信息'][0] == "是":
    LITE_MODE = True
else:
    LITE_MODE = False

print('当前引擎:', DRIVER)
print('简略模式:', LITE_MODE)
KEY = dict(verifyKey=KEY)

# 连接bot
SESSION, _ = botlink.linkbot(key=KEY, host=HOST, botqq=BOT_QQ)
print('启用该功能的群:', GROUPS)

# 打开浏览器, 准备截图
OPTIONS = ChromeOptions()
OPTIONS.add_argument('--disable-software-rasterizer')
OPTIONS.add_argument('-ignore-certificate-errors')
OPTIONS.add_argument('--headless')
OPTIONS.add_argument('--disable-gpu')
OPTIONS.add_argument('--no-sandbox')

WEB_DRIVER = webdriver.Chrome(options=OPTIONS)
WEB_DRIVER.get('https://baike.sogou.com/')
print("Launch successful")

# 开始监听会话
while True:
    msg = simuse.fetch_message(host=HOST, session=SESSION, deal=1)

    if msg == 0:
        continue
    try:
        group = msg[0]['group']
        sender = msg[0]['sender']
        msg = msg[0]['messagechain'][1]['text']

        if str(group) not in str(GROUPS):
            continue

        # 检查监听内容
        if "百科 " in msg:  # 搜索百科
            keyword = msg.replace('百科 ', '')
            img = 0
            if LITE_MODE:
                msg_sender.send_str(group=group, session=SESSION, message='简略模式搜索中....', host=HOST)

                # 获取图片
                if DRIVER == "搜狗百科":
                    img = sougou_spider.search_less(web=WEB_DRIVER, word=keyword)
                elif DRIVER == "萌娘百科":
                    img = moegirl_spider.search_less(web=WEB_DRIVER, word=keyword)
                else:
                    raise Exception("WTF? 你填了什么?")
            else:
                msg_sender.send_str(group=group, session=SESSION, message='详细模式搜索中....等待时间可能较长',
                                host=HOST)

                # 获取图片
                if DRIVER == "搜狗百科":
                    img = sougou_spider.search_more(web=WEB_DRIVER, word=keyword)
                elif DRIVER == "萌娘百科":
                    img = moegirl_spider.search_more(web=WEB_DRIVER, word=keyword)
                else:
                    raise Exception("WTF? 你填了什么?")

                # 检查图片
                if img == 0:
                    msg_sender.send_str(group=group, session=SESSION, message='搜索出错，该词条未收录', host=HOST)
                    continue
            # 检查图片
            if img == 0:
                msg_sender.send_str(group=group, session=SESSION, message='搜索出错，该词条未收录', host=HOST)
                continue

            print('Sending Image..')
            t1 = time.time()
            msg_sender.send_image(group=group, session=SESSION, message=img, host=HOST)
            print('Sent! [{}s]'.format(time.time() - t1))
        elif '/切换模式' in msg:  # 更换搜索模式
            if sender in ADMIN_QQ:
                LITE_MODE = not LITE_MODE
                msg_sender.send_str(group=group, session=SESSION, message='切换成功', host=HOST)
            else:
                msg_sender.send_str(group=group, session=SESSION, message='只有管理员可以切换模式', host=HOST)
        elif '/切换引擎' in msg:  # 更换搜索引擎
            if sender in ADMIN_QQ:
                if DRIVER == '搜狗百科':
                    DRIVER = '萌娘百科'
                    msg_sender.send_str(group=group, session=SESSION, message='当前引擎切换为萌娘百科', host=HOST)
                elif DRIVER == '萌娘百科':
                    DRIVER = '搜狗百科'
                    msg_sender.send_str(group=group, session=SESSION, message='当前引擎切换为搜狗百科', host=HOST)
                    WEB_DRIVER.get('https://baike.sogou.com/')
            else:
                msg_sender.send_str(group=group, session=SESSION, message='只有管理员可以切换引擎', host=HOST)
    except Exception as e:
        print('发生了一个错误: '+str(e))

    time.sleep(1)
