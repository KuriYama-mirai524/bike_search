import requests as r


def send_image(group, session, message, host):
    data = dict(sessionKey=session, target=group, messageChain=[dict(type='Image', base64=message)])
    resp = r.request('post', host + '/sendGroupMessage', json=data)
    print(resp.json())


def send_str(group, session, message, host):
    data = dict(sessionKey=session, target=group, messageChain=[dict(type='Plain', text=message)])
    resp = r.request('post', host + '/sendGroupMessage', json=data)
    print(resp.json())
