import json
import random
import re
import time
from time import sleep

import requests
from lxml import etree


# 公共的header，模拟请求的客户端
user_agent = [
    "Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_8; en-us) AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 Safari/534.50",
    "Mozilla/5.0 (Windows; U; Windows NT 6.1; en-us) AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 Safari/534.50",
    "Mozilla/5.0 (Windows NT 10.0; WOW64; rv:38.0) Gecko/20100101 Firefox/38.0",
    "Mozilla/5.0 (Windows NT 10.0; WOW64; Trident/7.0; .NET4.0C; .NET4.0E; .NET CLR 2.0.50727; .NET CLR 3.0.30729; .NET CLR 3.5.30729; InfoPath.3; rv:11.0) like Gecko",
    "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0)",
    "Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.0; Trident/4.0)",
    "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0)",
    "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1)",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.6; rv:2.0.1) Gecko/20100101 Firefox/4.0.1",
    "Mozilla/5.0 (Windows NT 6.1; rv:2.0.1) Gecko/20100101 Firefox/4.0.1",
    "Opera/9.80 (Macintosh; Intel Mac OS X 10.6.8; U; en) Presto/2.8.131 Version/11.11",
    "Opera/9.80 (Windows NT 6.1; U; en) Presto/2.8.131 Version/11.11",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_0) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.56 Safari/535.11",
    "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Maxthon 2.0)",
    "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; TencentTraveler 4.0)",
    "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)",
    "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; The World)",
    "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Trident/4.0; SE 2.X MetaSr 1.0; SE 2.X MetaSr 1.0; .NET CLR 2.0.50727; SE 2.X MetaSr 1.0)",
    "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; 360SE)",
    "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Avant Browser)",
    "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)",
    "Mozilla/5.0 (iPhone; U; CPU iPhone OS 4_3_3 like Mac OS X; en-us) AppleWebKit/533.17.9 (KHTML, like Gecko) Version/5.0.2 Mobile/8J2 Safari/6533.18.5",
    "Mozilla/5.0 (iPod; U; CPU iPhone OS 4_3_3 like Mac OS X; en-us) AppleWebKit/533.17.9 (KHTML, like Gecko) Version/5.0.2 Mobile/8J2 Safari/6533.18.5",
    "Mozilla/5.0 (iPad; U; CPU OS 4_3_3 like Mac OS X; en-us) AppleWebKit/533.17.9 (KHTML, like Gecko) Version/5.0.2 Mobile/8J2 Safari/6533.18.5",
    "Mozilla/5.0 (Linux; U; Android 2.3.7; en-us; Nexus One Build/FRF91) AppleWebKit/533.1 (KHTML, like Gecko) Version/4.0 Mobile Safari/533.1",
    "MQQBrowser/26 Mozilla/5.0 (Linux; U; Android 2.3.7; zh-cn; MB200 Build/GRJ22; CyanogenMod-7) AppleWebKit/533.1 (KHTML, like Gecko) Version/4.0 Mobile Safari/533.1",
    "Opera/9.80 (Android 2.3.4; Linux; Opera Mobi/build-1107180945; U; en-GB) Presto/2.8.149 Version/11.10",
    "Mozilla/5.0 (Linux; U; Android 3.0; en-us; Xoom Build/HRI39) AppleWebKit/534.13 (KHTML, like Gecko) Version/4.0 Safari/534.13",
    "Mozilla/5.0 (BlackBerry; U; BlackBerry 9800; en) AppleWebKit/534.1+ (KHTML, like Gecko) Version/6.0.0.337 Mobile Safari/534.1+",
    "Mozilla/5.0 (hp-tablet; Linux; hpwOS/3.0.0; U; en-US) AppleWebKit/534.6 (KHTML, like Gecko) wOSBrowser/233.70 Safari/534.6 TouchPad/1.0",
    "Mozilla/5.0 (SymbianOS/9.4; Series60/5.0 NokiaN97-1/20.0.019; Profile/MIDP-2.1 Configuration/CLDC-1.1) AppleWebKit/525 (KHTML, like Gecko) BrowserNG/7.1.18124",
    "Mozilla/5.0 (compatible; MSIE 9.0; Windows Phone OS 7.5; Trident/5.0; IEMobile/9.0; HTC; Titan)",
    "UCWEB7.0.2.37/28/999",
    "NOKIA5700/ UCWEB7.0.2.37/28/999",
    "Openwave/ UCWEB7.0.2.37/28/999",
    "Mozilla/4.0 (compatible; MSIE 6.0; ) Opera/UCWEB7.0.2.37/28/999",
    # iPhone 6：
    "Mozilla/6.0 (iPhone; CPU iPhone OS 8_0 like Mac OS X) AppleWebKit/536.26 (KHTML, like Gecko) Version/8.0 Mobile/10A5376e Safari/8536.25",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/132.0.0.0 Safari/537.36 Edg/132.0.0.0"
]


class ProxyFetcher(object):
    """
    各种同步、获取代理的方法
    """

    def __init__(self):
        super(ProxyFetcher, self).__init__()

    @staticmethod
    def freeProxy_zdaye():
        """
        站大爷 https://www.zdaye.com/dayProxy.html
        """
        host = f'https://www.zdaye.com'
        headers = {
            'User-Agent': random.choice(user_agent),
            'X-Forwarded-For': f'221.237.{random.randint(18, 68)}.{random.randint(23, 85)}',  # 有些网站可以伪造IP访问（防止反爬），如站大爷
            "Host": 'www.zdaye.com',
            'Referer': host,
        }
        try:
            list_page_uri = f'{host}/dayProxy.html'
            list_page_resp = requests.get(list_page_uri, verify=False, headers=headers)
            # 获取最新一篇可用代理的文章
            list_page_tree = etree.HTML(list_page_resp.text)
            # 提取特定 class=content 的 div下的 arctitle
            last_content_title = list_page_tree.xpath('//div[@class="content"]')[0].xpath('.//div[@class="arctitle"]/a')[0]
            last_page_uri = last_content_title.get('href').strip()
            print(f'获取{last_content_title.text.strip()}')
            # last_page_resp = requests.get(f'{host}{last_page_uri}', verify=False, headers={"User-Agent": random.choice(user_agent), "Host": host, "Referer": list_page_uri})
            last_page_resp = requests.get(f'{host}{last_page_uri}', verify=False, headers=headers)
            last_page_tree = etree.HTML(last_page_resp.text)
            # 提取id="ipc"的table的数据
            proxy_table = last_page_tree.xpath('//table[@id="ipc"]')[0]
            for tr in proxy_table.xpath('.//tr'):
                ip = "".join(tr.xpath("./td[1]/text()")).strip()
                port = "".join(tr.xpath("./td[2]/text()")).strip()
                scheme = "".join(tr.xpath("./td[3]/text()")).strip()
                anonymous = "".join(tr.xpath("./td[4]/text()")).strip()
                address = "".join(tr.xpath("./td[5]/text()")).strip()
                if not ip:
                    continue
                yield f'{ip}:{port}'
        except Exception as e:
            print('freeProxy_zdaye', e)

    @staticmethod
    def freeProxy_ihuan():
        """
        小幻代理 https://ip.ihuan.me
        """
        host = 'https://ip.ihuan.me'
        request_ip = f'221.237.{random.randint(18, 68)}.{random.randint(23, 85)}'  # 有些网站可以伪造IP访问（防止反爬），如站大爷
        one_user_agent = random.choice(user_agent)
        headers = {
            'User-Agent': one_user_agent,
            'X-Forwarded-For': request_ip,
            'Referer': host,
        }
        try:
            session_rq = requests.session()
            # 1. 先登录https://ip.ihuan.me/ti.html获取session
            login_resp = session_rq.get(f'{host}/ti.html', verify=False, headers=headers)
            if login_resp.status_code != 200:
                session_rq.headers.update({
                    'User-Agent': one_user_agent,
                    'X-Forwarded-For': request_ip,
                    'Referer': host,
                })
                login_resp = session_rq.get(f'{host}/ti.html', verify=False)
            # 2. 再获取查询key https://ip.ihuan.me/mouse.do
            session_rq.headers.update({
                'Referer': f'{host}/ti.html',
            })
            mouse_resp = session_rq.get(f'{host}/mouse.do', verify=False)
            # 正则查找匹配获取key
            match = re.search(r'\$\(\"input\[name=\'key\'\]\"\)\.val\(\"([a-fA-F0-9]+)\"\)', mouse_resp.text)
            if match:
                key = match.group(1)
            # 3. 最后再执行查询操作，先查国内，再查询国外https://ip.ihuan.me/tqdl.html
            session_rq.headers.update({
                "Origin": host,
            })
            paramss = [{
                'num': '3000',
                'port': '',
                'kill_port': '',
                'address': '中国',
                'kill_address': '',
                'anonymity': '',
                'type': '',
                'post': '',
                'sort': '',
                'key': key,
            },{
                'num': '3000',
                'port': '',
                'kill_port': '',
                'address': '',
                'kill_address': '中国',
                'anonymity': '',
                'type': '',
                'post': '',
                'sort': '',
                'key': key,
            },]
            for params in paramss:
                list_ip_resp = session_rq.post(f'{host}/tqdl.html', verify=False, data=params)
                list_ip_tree = etree.HTML(list_ip_resp.text)
                # 获取 <div class="panel-body"> 的文本内容
                panel_body = list_ip_tree.xpath('//div[@class="col-md-10"]/div[@class="panel panel-default"]/div[@class="panel-body"]/text()')
                for proxy_str in panel_body:
                    if proxy_str := proxy_str.strip():
                        # proxy = proxy_str.split(":")
                        yield proxy_str
        except Exception as e:
            print('freeProxy_ihuan', e)

    @staticmethod
    def freeProxy_89():
        """
        89免费代理 https://www.89ip.cn/
        """
        host = 'www.89ip.cn'
        headers = {
            'User-Agent': random.choice(user_agent),
            'X-Forwarded-For': f'221.237.{random.randint(18, 68)}.{random.randint(23, 85)}',  # 有些网站可以伪造IP访问（防止反爬），如站大爷
            "Host": host,
            "Referer": f'https://{host}/ti.html',
        }
        try:
            list_ip_resp = requests.get(f'https://{host}/tqdl.html?num=9999&address=&kill_address=&port=&kill_port=&isp=', verify=False, headers=headers)
            list_ip_tree = etree.HTML(list_ip_resp.text)
            # 获取 <div style="padding-left:20px;"> 的内容
            panel_body = list_ip_tree.xpath('//div[@style="padding-left:20px;"]/text()')
            for proxy_str in panel_body:
                if proxy_str := proxy_str.strip():
                    yield proxy_str
        except Exception as e:
            print('freeProxy_89', e)

    @staticmethod
    def freeProxy_ip3366():
        """
        齐云代理 https://proxy.ip3366.net/
        """
        host = 'proxy.ip3366.net'
        headers = {
            'User-Agent': random.choice(user_agent),
            'X-Forwarded-For': f'221.237.{random.randint(18, 68)}.{random.randint(23, 85)}',  # 有些网站可以伪造IP访问（防止反爬），如站大爷
            "Host": host,
            "Referer": f'https://{host}/',
        }
        page = 1  # 从第一页开始
        while True:
            try:
                list_ip_resp = requests.get(f'https://{host}/free/?action=china&page={page}', verify=False, headers=headers)
                list_ip_tree = etree.HTML(list_ip_resp.text)
                # 提取id="ipc"的table的数据
                proxy_table = list_ip_tree.xpath('//table')[0]
                tr_list = proxy_table.xpath('.//tr')
                if len(tr_list) <= 1:
                    return
                for tr in tr_list:
                    ip = "".join(tr.xpath("./td[1]/text()")).strip()
                    port = "".join(tr.xpath("./td[2]/text()")).strip()
                    anonymous = "".join(tr.xpath("./td[3]/text()")).strip()
                    scheme = "".join(tr.xpath("./td[4]/text()")).strip()
                    address = "".join(tr.xpath("./td[5]/text()")).strip()
                    if not ip:
                        continue
                    yield f'{ip}:{port}'
                page += 1
                # 先暂停一下，避免反爬
                sleep(0.1)
            except Exception as e:
                print('freeProxy_ip3366', e)

    @staticmethod
    def freeProxy_kxdaili():
        """
        开心代理 http://www.kxdaili.com/
        """
        host = 'www.kxdaili.com'
        headers = {
            'User-Agent': random.choice(user_agent),
            'X-Forwarded-For': f'221.237.{random.randint(18, 68)}.{random.randint(23, 85)}',  # 有些网站可以伪造IP访问（防止反爬），如站大爷
            "Host": host,
            "Referer": f'https://{host}/',
        }
        # 高匿代理
        page = 1  # 从第一页开始
        while True:
            try:
                list_ip_resp = requests.get(f'http://{host}/dailiip/1/{page}.html', verify=False, headers=headers)
                list_ip_tree = etree.HTML(list_ip_resp.content.decode('utf-8'))
                # 提取table的数据
                list_ip_table = list_ip_tree.xpath('//table')
                if not list_ip_table:
                    break
                proxy_table = list_ip_table[0]
                tr_list = proxy_table.xpath('.//tr')
                for tr in tr_list:
                    ip = "".join(tr.xpath("./td[1]/text()")).strip()
                    port = "".join(tr.xpath("./td[2]/text()")).strip()
                    anonymous = "".join(tr.xpath("./td[3]/text()")).strip()
                    scheme = "".join(tr.xpath("./td[4]/text()")).strip()
                    address = "".join(tr.xpath("./td[6]/text()")).strip()
                    if not ip:
                        continue
                    yield f'{ip}:{port}'
                page += 1
                # 先暂停一下，避免反爬
                sleep(0.1)
            except Exception as e:
                print('freeProxy_kxdaili 1', e)
        # 普通代理，如果不需要，可以注释以下代码
        page = 1  # 从第一页开始
        while True:
            try:
                list_ip_resp = requests.get(f'http://{host}/dailiip/2/{page}.html', verify=False, headers=headers)
                list_ip_tree = etree.HTML(list_ip_resp.content.decode('utf-8'))
                # 提取table的数据
                list_ip_table = list_ip_tree.xpath('//table')
                if not list_ip_table:
                    return
                proxy_table =list_ip_table[0]
                tr_list = proxy_table.xpath('.//tr')
                for tr in tr_list:
                    ip = "".join(tr.xpath("./td[1]/text()")).strip()
                    port = "".join(tr.xpath("./td[2]/text()")).strip()
                    anonymous = "".join(tr.xpath("./td[3]/text()")).strip()
                    scheme = "".join(tr.xpath("./td[4]/text()")).strip()
                    address = "".join(tr.xpath("./td[6]/text()")).strip()
                    if not ip:
                        continue
                    yield f'{ip}:{port}'
                page += 1
                # 先暂停一下，避免反爬
                sleep(0.1)
            except Exception as e:
                print('freeProxy_kxdaili 2', e)

    @staticmethod
    def freeProxy_ip3366_2():
        """
        云代理 http://www.ip3366.net/
        """
        host = 'www.ip3366.net'
        headers = {
            'User-Agent': random.choice(user_agent),
            'X-Forwarded-For': f'221.237.{random.randint(18, 68)}.{random.randint(23, 85)}',  # 有些网站可以伪造IP访问（防止反爬），如站大爷
            "Host": host,
            "Referer": f'https://{host}/',
        }
        # 高匿代理
        page = 1  # 从第一页开始
        while True:
            try:
                if page == 8:
                    break
                list_ip_resp = requests.get(f'http://{host}/?stype=1&page=1', verify=False, headers=headers)
                list_ip_tree = etree.HTML(list_ip_resp.content.decode('gb2312'))
                # 提取table的数据
                proxy_table = list_ip_tree.xpath('//table')[0]
                tr_list = proxy_table.xpath('.//tr')
                for tr in tr_list:
                    ip = "".join(tr.xpath("./td[1]/text()")).strip()
                    port = "".join(tr.xpath("./td[2]/text()")).strip()
                    anonymous = "".join(tr.xpath("./td[3]/text()")).strip()
                    scheme = "".join(tr.xpath("./td[4]/text()")).strip()
                    address = "".join(tr.xpath("./td[5]/text()")).strip()
                    if not ip:
                        continue
                    yield f'{ip}:{port}'
                page += 1
                # 先暂停一下，避免反爬
                sleep(0.1)
            except Exception as e:
                print('freeProxy_ip3366_2 1', e)
        # 普通代理，如果不需要，可以注释以下代码
        page = 1  # 从第一页开始
        while True:
            try:
                if page == 8:
                    return
                list_ip_resp = requests.get(f'http://{host}/?stype=2&page={page}', verify=False, headers=headers)
                list_ip_tree = etree.HTML(list_ip_resp.content.decode('gb2312'))
                # 提取table的数据
                proxy_table = list_ip_tree.xpath('//table')[0]
                tr_list = proxy_table.xpath('.//tr')
                for tr in tr_list:
                    ip = "".join(tr.xpath("./td[1]/text()")).strip()
                    port = "".join(tr.xpath("./td[2]/text()")).strip()
                    anonymous = "".join(tr.xpath("./td[3]/text()")).strip()
                    scheme = "".join(tr.xpath("./td[4]/text()")).strip()
                    address = "".join(tr.xpath("./td[5]/text()")).strip()
                    if not ip:
                        continue
                    yield f'{ip}:{port}'
                page += 1
                # 先暂停一下，避免反爬
                sleep(0.1)
            except Exception as e:
                print('freeProxy_ip3366_2 2', e)

    @staticmethod
    def freeProxy_kuaidaili():
        """
        快代理 https://www.kuaidaili.com/
        """
        host = 'www.kuaidaili.com'
        headers = {
            'User-Agent': random.choice(user_agent),
            'X-Forwarded-For': f'221.237.{random.randint(18, 68)}.{random.randint(23, 85)}',  # 有些网站可以伪造IP访问（防止反爬），如站大爷
            "Host": host,
            "Referer": f'https://{host}/',
        }
        pattern = r"const fpsList = (\[.*?\]);"
        # 国内高匿代理
        page = 1  # 从第一页开始
        while True:
            try:
                list_ip_resp = requests.get(f'http://{host}/free/inha/{page}/', verify=False, headers=headers)
                # 使用正则表达式提取数据
                match = re.search(pattern, list_ip_resp.text)
                if match:
                    # 提取 JSON 字符串
                    json_str = match.group(1)
                    # 解析 JSON 字符串为 Python 列表
                    fps_list = json.loads(json_str)
                    for item in fps_list:
                        ip = item['ip']
                        port = item['port']
                        anonymous = '高匿名'
                        scheme = 'HTTP'
                        address = item['location']
                        if not ip:
                            continue
                        yield f'{ip}:{port}'
                else:
                    print("freeProxy_kuaidaili 国内高匿代理 未找到 JSON 数据", page)
                    break
                page += 1
                # 先暂停一下，避免反爬
                sleep(0.1)
            except Exception as e:
                print('freeProxy_kuaidaili inha', e)
        # 国内普通代理，如果不需要，可以注释以下代码
        page = 1  # 从第一页开始
        while True:
            try:
                list_ip_resp = requests.get(f'http://{host}/free/intr/{page}/', verify=False, headers=headers)
                # 使用正则表达式提取数据
                match = re.search(pattern, list_ip_resp.text)
                if match:
                    # 提取 JSON 字符串
                    json_str = match.group(1)
                    # 解析 JSON 字符串为 Python 列表
                    fps_list = json.loads(json_str)
                    for item in fps_list:
                        ip = item['ip']
                        port = item['port']
                        anonymous = '高匿名'
                        scheme = 'HTTP'
                        address = item['location']
                        if not ip:
                            continue
                        yield f'{ip}:{port}'
                else:
                    print("freeProxy_kuaidaili 国内普通代理 未找到 JSON 数据", page)
                    break
                page += 1
                # 先暂停一下，避免反爬
                sleep(0.1)
            except Exception as e:
                print('freeProxy_kuaidaili intr', e)
        # 海外代理
        page = 1  # 从第一页开始
        while True:
            try:
                list_ip_resp = requests.get(f'http://{host}/free/fps/{page}/', verify=False, headers=headers)
                # 使用正则表达式提取数据
                match = re.search(pattern, list_ip_resp.text)
                if match:
                    # 提取 JSON 字符串
                    json_str = match.group(1)
                    # 解析 JSON 字符串为 Python 列表
                    fps_list = json.loads(json_str)
                    for item in fps_list:
                        ip = item['ip']
                        port = item['port']
                        anonymous = '高匿名'
                        scheme = 'HTTP'
                        address = item['location']
                        if not ip:
                            continue
                        yield f'{ip}:{port}'
                else:
                    print("freeProxy_kuaidaili 海外代理 未找到 JSON 数据", page)
                    return
                page += 1
                # 先暂停一下，避免反爬
                sleep(0.1)
            except Exception as e:
                print('freeProxy_kuaidaili intr', e)

    @staticmethod
    def freeProxy_proxy_list():
        """
        proxy-list https://www.proxy-list.download/api/v1
        type (required)	http, https, socks4, socks5	?type=http
        anon (optional)	transparent, anonymous, elite	?type=http&anon=elite
        country (optional)	Country ISO code	?type=http&country=US
        """
        host = 'www.proxy-list.download'
        headers = {
            'User-Agent': random.choice(user_agent),
            'X-Forwarded-For': f'221.237.{random.randint(18, 68)}.{random.randint(23, 85)}',  # 有些网站可以伪造IP访问（防止反爬），如站大爷
            "Host": host,
            "Referer": f'https://{host}/',
        }
        try:
            # 先获取http
            list_ip_resp = requests.get(f'https://{host}/api/v1/get?type=http', verify=False, headers=headers)
            # 获取返回的内容，按行拆分
            proxy_str_lines = list_ip_resp.text.strip().split('\n')
            for proxy_str in proxy_str_lines:
                if proxy_str := proxy_str.strip():
                    yield proxy_str
            # 再获取https
            list_ip_resp = requests.get(f'https://{host}/api/v1/get?type=https', verify=False, headers=headers)
            # 获取返回的内容，按行拆分
            proxy_str_lines = list_ip_resp.text.strip().split('\n')
            for proxy_str in proxy_str_lines:
                if proxy_str := proxy_str.strip():
                    yield proxy_str
        except Exception as e:
            print('freeProxy_proxy_list', e)

    @staticmethod
    def freeProxy_free_proxy_list():
        """
        free-proxy-list https://free-proxy-list.net
        """
        host = 'free-proxy-list.net'
        headers = {
            'User-Agent': random.choice(user_agent),
            'X-Forwarded-For': f'221.237.{random.randint(18, 68)}.{random.randint(23, 85)}',  # 有些网站可以伪造IP访问（防止反爬），如站大爷
            "Host": host,
            "Referer": f'https://{host}/',
        }
        try:
            list_ip_resp = requests.get(f'https://{host}', verify=False, headers=headers)
            list_ip_tree = etree.HTML(list_ip_resp.text)
            # 提取id="ipc"的table的数据
            proxy_table = list_ip_tree.xpath('//div[@class="table-responsive fpl-list"]/table')[0]
            tr_list = proxy_table.xpath('.//tr')
            for tr in tr_list:
                ip = "".join(tr.xpath("./td[1]/text()")).strip()
                port = "".join(tr.xpath("./td[2]/text()")).strip()
                anonymous = "".join(tr.xpath("./td[5]/text()")).strip()
                scheme = "".join(tr.xpath("./td[7]/text()")).strip()
                address = "".join(tr.xpath("./td[4]/text()")).strip()
                if not ip:
                    continue
                yield f'{ip}:{port}'
        except Exception as e:
            print('freeProxy_free_proxy_list', e)

    @staticmethod
    def freeProxy_spys():
        """
        spys https://spys.me/
        """
        host = 'spys.me'
        headers = {
            'User-Agent': random.choice(user_agent),
            'X-Forwarded-For': f'221.237.{random.randint(18, 68)}.{random.randint(23, 85)}',  # 有些网站可以伪造IP访问（防止反爬），如站大爷
            "Host": host,
            "Referer": f'https://{host}/',
        }
        try:
            # 先获取http
            list_ip_resp = requests.get(f'https://{host}/proxy.txt', verify=False, headers=headers)
            # 使用正则表达式提取 IP:Port，按行拆分
            proxy_str_lines = re.findall(r'\b(?:\d{1,3}\.){3}\d{1,3}:\d+\b', list_ip_resp.text)
            for proxy_str in proxy_str_lines:
                if proxy_str := proxy_str.strip():
                    yield proxy_str
        except Exception as e:
            print('freeProxy_spys', e)

    @staticmethod
    def freeProxy_proxy_daily():
        """
        proxy-daily https://proxy-daily.com/
        """
        host = 'proxy-daily.com'
        headers = {
            'User-Agent': random.choice(user_agent),
            'X-Forwarded-For': f'221.237.{random.randint(18, 68)}.{random.randint(23, 85)}',  # 有些网站可以伪造IP访问（防止反爬），如站大爷
            "Host": host,
            "Referer": f'https://{host}/',
        }
        try:
            list_ip_resp = requests.get(f'https://{host}/api/serverside/proxies?draw=1&columns%5B0%5D%5Bdata%5D=ip&columns%5B0%5D%5Bname%5D=ip&columns%5B0%5D%5Bsearchable%5D=true&columns%5B0%5D%5Borderable%5D=false&columns%5B0%5D%5Bsearch%5D%5Bvalue%5D=&columns%5B0%5D%5Bsearch%5D%5Bregex%5D=false&columns%5B1%5D%5Bdata%5D=port&columns%5B1%5D%5Bname%5D=port&columns%5B1%5D%5Bsearchable%5D=true&columns%5B1%5D%5Borderable%5D=false&columns%5B1%5D%5Bsearch%5D%5Bvalue%5D=&columns%5B1%5D%5Bsearch%5D%5Bregex%5D=false&columns%5B2%5D%5Bdata%5D=protocol&columns%5B2%5D%5Bname%5D=protocol&columns%5B2%5D%5Bsearchable%5D=true&columns%5B2%5D%5Borderable%5D=false&columns%5B2%5D%5Bsearch%5D%5Bvalue%5D=&columns%5B2%5D%5Bsearch%5D%5Bregex%5D=false&columns%5B3%5D%5Bdata%5D=speed&columns%5B3%5D%5Bname%5D=speed&columns%5B3%5D%5Bsearchable%5D=true&columns%5B3%5D%5Borderable%5D=false&columns%5B3%5D%5Bsearch%5D%5Bvalue%5D=&columns%5B3%5D%5Bsearch%5D%5Bregex%5D=false&columns%5B4%5D%5Bdata%5D=anonymity&columns%5B4%5D%5Bname%5D=anonymity&columns%5B4%5D%5Bsearchable%5D=true&columns%5B4%5D%5Borderable%5D=false&columns%5B4%5D%5Bsearch%5D%5Bvalue%5D=&columns%5B4%5D%5Bsearch%5D%5Bregex%5D=false&columns%5B5%5D%5Bdata%5D=country&columns%5B5%5D%5Bname%5D=country&columns%5B5%5D%5Bsearchable%5D=true&columns%5B5%5D%5Borderable%5D=false&columns%5B5%5D%5Bsearch%5D%5Bvalue%5D=&columns%5B5%5D%5Bsearch%5D%5Bregex%5D=false&start=0&length=10000&search%5Bvalue%5D=&search%5Bregex%5D=false&_={time.time()}', verify=False, headers=headers)
            for proxy_data in list_ip_resp.json()['data']:
                ip = proxy_data['ip']
                port = proxy_data['port']
                anonymous = proxy_data['anonymity']
                scheme = proxy_data['protocol']
                address = proxy_data['country']
                yield f'{ip}:{port}'
        except Exception as e:
            print('freeProxy_proxy_daily', e)
