import urllib.request as request

from bs4 import BeautifulSoup


class myproxy(object):
    current_proxy_index = -1
    urls = []

    def __init__(self):
        dom = request.urlopen('http://www.kuaidaili.com/').read()
        soup = BeautifulSoup(dom, 'lxml')
        tbody = soup.table.tbody

        for tr in tbody.find_all('tr'):
            self.urls.append(tr.find_all('td')[0].get_text() + ':' + tr.find_all('td')[1].get_text())

        self.switch()
        self.open()

    def switch(self):
        self.current_proxy_index += 1
        if self.current_proxy_index >= len(self.urls):
            self.current_proxy_index = 0

        proxy = request.ProxyHandler({'http': self.urls[self.current_proxy_index]})
        auth = request.HTTPBasicAuthHandler()
        opener = request.build_opener(proxy, auth, request.HTTPHandler)
        request.install_opener(opener)

        print('switch to ' + self.urls[self.current_proxy_index])

    def open(self):
        headers = {
            'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'Accept-Encoding': 'gzip, deflate',
            'Host': 'www.lagou.com',
            'Origin': 'http://www.lagou.com',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.116 Safari/537.36',
            'X-Requested-With': 'XMLHttpRequest',
            'Referer': 'https://www.lagou.com',
            'Proxy-Connection': 'keep-alive',
            'X-Anit-Forge-Code': '0',
            'X-Anit-Forge-Token': None
        }
        while True:
            try:
                # req = request.Request(url='https://www.lagou.com/', headers=headers)
                req = request.Request(url='https://www.lagou.com/', headers={})
                # req = request.Request(url='http://www.baidu.com/', headers={})
                # req = request.Request(url='http://blog.csdn.net/', headers={})
                # req = request.Request(url='http://www.google.com/', headers=headers)
                print(request.urlopen(req).read())
                break
            except Exception as e:
                print(e)
                self.switch()


if __name__ == '__main__':
    myproxy()
