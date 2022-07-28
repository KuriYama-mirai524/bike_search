
import requests as r


def sendmessage_img(group, session, message, host):
    data = dict(sessionKey=session, target=group, messageChain=[dict(type='Image', base64=message)])
    resp = r.request('post', host+'/sendGroupMessage', json=data)
    print(resp.json())

def sendmessage_txt(group, session, message, host):
    data = dict(sessionKey=session, target=group, messageChain=[dict(type='Plain', text=message)])
    resp = r.request('post', host+'/sendGroupMessage', json=data)
    print(resp.json())
