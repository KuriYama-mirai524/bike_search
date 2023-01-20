import requests


def linkbot(key, botqq, host):
    # 连接到bot
    resp = requests.request('post', host + '/verify', json=key)
    print('获取会话...')
    if resp.json()['code'] == 400:
        print('会话获取失败,请检查端口或key')
    else:
        session = resp.json()['session']
        data = dict(sessionKey=resp.json()['session'], qq=botqq)
        resp = requests.request('post', host + '/bind', json=data)
        print(resp.json())
        if resp.json()['code'] == 0:
            print('bot连接成功!')
        else:
            print('连接失败')
    return session, host
