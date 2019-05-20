# -*- coding: utf-8 -*-
import requests
from lxml import etree

cookie = "JSESSIONID=BC3C8927E8890A42ED1A10F8847B106A"
barCode = '02557936'
data = {}


#我的借阅界面，将书名和其条形码拿出来
def borrow(data,cookies):
    '''

    :param data: 空字典，存书名和对应的条形码
    :param cookies: cookie
    :return: 书名和条形码组成的data
    '''
    baseurl = "http://opac.jnu.edu.cn/opac/mylibrary/borrowBooks"
    baseheaders = {
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.131 Safari/537.36",
        "Connection": "keep-alive"
    }
    jar = requests.cookies.RequestsCookieJar()
    for cookie1 in cookies.split(';'):
        key, value = cookie1.split('=', 1)
        jar.set(key, value)
    rsp = requests.get(baseurl, headers=baseheaders,cookies = jar)
    rsp = rsp.content.decode()
    #print(rsp)
    html = etree.HTML(rsp)
    html_data = html.xpath('//tr')
    for i in range(1,len(html_data)):
        data1 = html_data[i].xpath('//td[2]/a/text()')
        data2 = html_data[i].xpath('//td[3]/text()')
        #print(data1[i-1],data2[i-1])
        data[data1[i-1]] = data2[i-1]
    return data


#续借功能
def renew(barcode,cookies):
    '''

    :param barcode: 条形码
    :param cookies: cookie
    :return: 0 : 成功
             1 : 加载失败
             2 : 续借超次数
    '''
    success = '{"errorMessage":"续借成功","successed":true}'
    renewurl = "http://opac.jnu.edu.cn/opac/mylibrary/renewBook"
    reheaders = {
        "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.131 Safari/537.36"
    }
    redata = {
        "barCode": barcode
    }
    jar = requests.cookies.RequestsCookieJar()
    for cookie1 in cookies.split(';'):
        key, value = cookie1.split('=', 1)
        jar.set(key, value)
    rsp = requests.post(renewurl, headers=reheaders,data = redata ,cookies = jar )
    if rsp.status_code != 200:
        print('网页加载失败QAQ')
        return 1
    rsp = rsp.content.decode()
    if rsp == success:
        print('续借成功~')
        return 0
    else:
        print('超过续借次数QAQ')
        return 2


borrow(data,cookie)
print(data)
a = renew(barCode,cookie)
print(a)
