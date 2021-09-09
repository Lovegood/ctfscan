#!/usr/bin/env python3
# -*- coding:utf8 -*-
__author__ = 'Cytosine'

import sys
import asyncio
import aiohttp
import requests

async def requests_get(url, normal_resp):
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            current_resp = await response.read()
            if response.status != 404 and normal_resp != current_resp:
                print(f'\033[1;32;40m[+] {response.status} {url}\033[0m')
            else:
                print(f'[-] 404 {url}')


def scan(host, filenames):
    filename_extension_dic = """
    .php.swp
    .php~
    .php.bak
    .php.old
    .php.swo
    .php.svn
    .php.zip
    .php.rar
    .php.txt
    ~
    ~1~
    ~2~
    ~3~
    .save
    .save1
    .save2
    .save3
    .bak_Edietplus
    .bak
    .back
    .war
    .phps
    """
    filename_extension_list = filename_extension_dic.strip().split()
    all_url = []
    for filename in filenames:
        for extension in filename_extension_list:
            all_url.append(f'{host}{filename}{extension}')
            all_url.append(f'{host}.{filename}{extension}')

    backup_and_version_dic = """
    .git/
    .svn/
    .hg/
    robots.txt
    1.zip
    1.rar
    tar.zip
    tar.rar
    web.zip
    web.rar
    web.tgz
    web1.zip
    web1.rar
    123.zip
    123.rar
    code.zip
    code.rar
    www.zip
    www.rar
    root.zip
    root.rar
    wwwroot.zip
    wwwroot.rar
    backup.zip
    backup.rar
    mysql.bak
    a.sql
    b.sql
    db.sql
    bdb.sql
    ddb.sql
    mysql.sql
    dump.sql
    data.sql
    backup.sql
    backup.sql.gz
    backup.sql.bz2
    backup.zip
    rss.xml
    crossdomain.xml
    phpinfo.php
    test.php
    .env
    """
    backup_and_version_list = backup_and_version_dic.strip().split()
    for b in backup_and_version_list:
        all_url.append(f'{host}{b}')

    normal_resp = requests.get(host).content
    
    loop = asyncio.get_event_loop()
    tasks = [requests_get(u, normal_resp) for u in all_url]
    loop.run_until_complete(asyncio.wait(tasks))
    loop.close()

    print('[*] Scan Finished.')

    pass


if __name__ == '__main__':  # 使用示例  $ python3 ctfscan2.py ctf.com index login register
    host = sys.argv[1]
    filename = sys.argv[2:]

    # host = 'localhost'
    # filename = ['index','login','register']

    if 'http' not in host:
        host = 'http://' + host

    if host[-1] != '/':
        host = host + '/'

    scan(host, filename)
