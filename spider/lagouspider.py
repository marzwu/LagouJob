import os
import time

import requests

from proxy import proxy
from util import toolkit

request_batch_count = 100
request_count = 0


def scrapy(jobname):
    urlproxy = proxy.myproxy()

    req_url = 'http://www.lagou.com/jobs/positionAjax.json?'
    headers = {
        # 'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
        # 'Accept-Encoding': 'gzip, deflate',
        # 'Host': 'www.lagou.com',
        # 'Origin': 'http://www.lagou.com',
        # 'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.116 Safari/537.36',
        # 'X-Requested-With': 'XMLHttpRequest',
        # 'Referer': 'http://www.lagou.com',
        # 'Proxy-Connection': 'keep-alive',
        # 'X-Anit-Forge-Code': '0',
        # 'X-Anit-Forge-Token': None

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
    # response = requests.post(req_url, params={'first': 'false', 'pn': 1, 'kd': jobname}, headers=headers)
    response = urlproxy.post(req_url, params={'first': 'false', 'pn': 1, 'kd': jobname}, headers=headers)
    try:
        maxpagenum = int(response.json()['content']['positionResult']['totalCount']) / 15
    except Exception as e:
        print(e)
        print(response)

    flag = True
    num = 1

    filedir = '../data/' + jobname

    if os.path.exists(filedir) is not True or os.path.isdir(filedir) is not True:
        os.mkdir(filedir)

    while flag:
        payload = {'first': 'false', 'pn': str(num), 'kd': jobname}

        # response = requests.post(req_url, params=payload, headers=headers)
        response = urlproxy.post(req_url, params=payload, headers=headers)
        if num > maxpagenum:
            flag = False

        if response.status_code == 200:
            try:
              job_json = response.json()['content']['positionResult']['result']
            except Exception as e:
                print(e)
                print(response)

            print('正在爬取第 ' + str(num) + ' 页的数据...')
            print(job_json)

            with open('../data/' + jobname + os.path.sep + str(num) + '.json', 'wt',
                      encoding='utf-8') as f:
                f.write(str(job_json))
                f.flush()
                f.close()

        else:
            print('connect error! url = ' + req_url)

        num += 1
        # time.sleep(2)

        global request_count, request_batch_count
        request_count += 1
        if request_count >= request_batch_count:
            request_count = 0
            urlproxy.switch()
            # print('sleep')
            # time.sleep(60)


if __name__ == '__main__':
    configmap = toolkit.readconfig('../job.xml')

    datapath = '../data'
    if not os.path.exists(datapath):
        os.mkdir(datapath)

    for item, value in configmap.items():
        for job in value:
            print('start crawl ' + str(job.parameter) + ' ...')
            scrapy(job.parameter)
