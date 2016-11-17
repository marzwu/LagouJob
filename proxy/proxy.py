import urllib.request as request

import requests
from bs4 import BeautifulSoup


def get_kuaidaili():
    dom = requests.get('http://www.kuaidaili.com/')
    soup = BeautifulSoup(dom.content, 'lxml')
    tbody = soup.table.tbody

    urls = []
    for tr in tbody.find_all('tr'):
        urls.append(tr.find_all('td')[0].get_text() + ':' + tr.find_all('td')[1].get_text())

    return urls


class myproxy(object):
    current_proxy_index = -1
    urls = []
    proxies = {}

    def __init__(self):
        self.urls = get_kuaidaili()

        self.switch()
        # self.open('')

    def switch(self):
        self.current_proxy_index += 1
        if self.current_proxy_index >= len(self.urls):
            self.current_proxy_index = 0

        self.proxies = {
            'http': 'http://' + self.urls[self.current_proxy_index]
        }

        proxy = request.ProxyHandler({'http': self.urls[self.current_proxy_index]})
        auth = request.HTTPBasicAuthHandler()
        opener = request.build_opener(proxy, auth, request.HTTPHandler)
        request.install_opener(opener)

        print('switch to ' + self.urls[self.current_proxy_index])

    def open(self, url, headers):
        while True:
            try:
                req = request.Request(url=url, headers=headers)
                # req = request.Request(url='https://www.lagou.com/', headers=headers)
                # req = request.Request(url='https://www.lagou.com/', headers={})
                # req = request.Request(url='http://www.baidu.com/', headers={})
                # req = request.Request(url='http://blog.csdn.net/', headers=headers)
                # req = request.Request(url='http://www.google.com/', headers=headers)
                print(request.urlopen(req).read())
                break
            except Exception as e:
                print(e)
                self.switch()

    def post(self, url, data=None, json=None, **kwargs):
        while True:
            try:
                kwargs['proxies'] = self.proxies
                return requests.post(url, kwargs)
            except Exception as e:
                print(e)
                self.switch()


if __name__ == '__main__':
    print(get_kuaidaili())

    headers = {
        # 'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
        # 'Accept-Encoding': 'gzip, deflate',
        # 'Host': 'www.lagou.com',
        # 'Origin': 'http://www.lagou.com',
        # 'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.116 Safari/537.36',
        # 'X-Requested-With': 'XMLHttpRequest',
        # 'Referer': 'https://www.lagou.com',
        # 'Proxy-Connection': 'keep-alive',
        # 'X-Anit-Forge-Code': '0',
        # 'X-Anit-Forge-Token': None

        # 'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        # 'Accept-Encoding': 'gzip, deflate, sdch',
        # 'Accept-Language': 'en-US,en;q=0.8',
        # 'Cache-Control': 'max-age=0',
        # 'Connection': 'keep-alive',
        # 'Cookie': 'bdshare_firstime=1459306894087; uuid_tt_dd=218275863771169932_20160330; lzstat_uv=3038750058275729362|3599678@2754945; _ga=GA1.2.2105376899.1465963919; UN=marzwu; UE="marzwu@gmail.com"; BT=1465963929287; uuid=eaa21bf8-efbf-4e7f-80b9-ec2bd22d6ba5; __message_district_code=310000; __message_sys_msg_id=0; __message_gu_msg_id=0; __message_cnel_msg_id=0; __message_in_school=0; Hm_lvt_6bcd52f51e9b3dce32bec4a3997715ac=1479352106,1479352601,1479352629,1479359797; Hm_lpvt_6bcd52f51e9b3dce32bec4a3997715ac=1479359797; dc_tos=ogrtbo; dc_session_id=1479359796756',
        # 'Host': 'blog.csdn.net',
        # 'Upgrade-Insecure-Requests': '1',
        # 'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.99 Safari/537.36 FirePHP/0.7.4'

        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Encoding': 'gzip, deflate, sdch, br',
        'Accept-Language': 'en-US,en;q=0.8',
        'Cache-Control': 'max-age=0',
        'Connection': 'keep-alive',
        # 'Cookie': 'user_trace_token=20161101142821-9a1b122dbb394e3a8a9c4d7457fbd64e; LGUID=20161101142822-636271ec-9ffc-11e6-bf56-525400f775ce; index_location_city=%E4%B8%8A%E6%B5%B7; LGMOID=20161116095636-25B5B594C4BFD95110DFD6014B7674EC; JSESSIONID=D531CC74191480247716B09D89536E7F; Hm_lvt_4233e74dff0ae5bd0a3d81c6ccf756e6=1478053294,1479281708,1479352888,1479355951; Hm_lpvt_4233e74dff0ae5bd0a3d81c6ccf756e6=1479360294; _gat=1; _ga=GA1.2.178559111.1477981701; LGSID=20161117132454-2bdc74d2-ac86-11e6-a4ec-5254005c3644; PRE_UTM=; PRE_HOST=; PRE_SITE=; PRE_LAND=https%3A%2F%2Fwww.lagou.com%2F; LGRID=20161117132454-2bdc7690-ac86-11e6-a4ec-5254005c3644',
        'Host': 'www.lagou.com',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.99 Safari/537.36 FirePHP/0.7.4'
    }

    _proxy = myproxy()
    _proxy.open('https://www.lagou.com/', headers)
