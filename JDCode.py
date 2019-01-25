import requests
import re
import time
import random
import json
import pymysql
import urllib.request

###全量地址数据
ip='111.72.107.240:36410'
headers={
 'user-agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36',
 'accept-encoding':'gzip, deflate, br'
}
oriurl='https://search.jd.com/Search?keyword=%E8%9C%82%E8%9C%9C&enc=utf-8&qrst=1&rt=1&stop=1&vt=2&wq=%E8%9C%82%E8%9C%9C&stock=1&page=3&s=60&click=0'

def GetComment(url,j,ip):
    print('---------正在采集商品评论')
    url = url.replace("page=3", "page=" + str(j))
    r = requests.get(url,proxies={'http':ip},headers=headers)
    ProductCodes = re.findall('href="//item.jd.com/(.*?)\.html', r.text)
    ProductCodes = list(set(ProductCodes))
    with open('comment.txt', 'a', encoding='utf-8') as ff:
        for ProductCode in ProductCodes:
            try:
                e = 'https://sclub.jd.com/comment/productPageComments.action?callback=fetchJSON_comment98vv15375&productId='
                f = '&score=0&sortType=5&page='
                r2 = '&score=0&sortType=5&page=0&pageSize=10&isShadowSku=0&fold=1'
                r3 = requests.get(e + str(ProductCode) + r2,proxies={'http':ip},headers=headers)
                data2 = json.loads(r3.text[27:-2])
                page = data2["maxPage"]
                for k in range(0, page):
                    h = '&pageSize=10&isShadowSku=0&fold=1'
                    html = urllib.request.urlopen(e + str(ProductCode) + f + str(k) + h).read().decode('gbk')
                    data3 = json.loads(html[27:-2])
                    for i in data3['comments']:
                        ProductCode = str(ProductCode)
                        try:
                            productColor = i['productColor']
                            content = i['content']
                            referenceTime = i['referenceTime']
                        except:
                            productColor = '0'
                            content = '0'
                            referenceTime = '0'
                        ff.write(str(ProductCode)+' '+str(content)+' '+str(productColor)+' '+str(referenceTime)+'\n')
            except:
                continue



def GetContent(url,j,BigType,SmallType1,ip):
    print('---------正在采集商品信息')
    url = url.replace("page=3", "page=" + str(j))
    r = requests.get(url,proxies={'http':ip},headers=headers)
    ProductCodes = re.findall('href="//item.jd.com/(.*?)\.html', r.text)
    ProductCodes = set(ProductCodes)
    with open('content.txt', 'a', encoding='utf-8') as fff:
        for ProductCode in ProductCodes:
            href = 'https://item.jd.com/' + str(ProductCode) + '.html'
            r = requests.get(href,proxies={'http':ip},headers=headers)
            html = r.text

            # 商品名称
            ProductName = re.findall(r'<div class="sku-name".*?>(.*?)</', r.text, re.S)[0].replace(' ','').replace('\n','')  if re.findall(r'<div class="sku-name">.*?>(.*?)</', r.text, re.S) else ''
            # print(ProductName)
            # 商品介绍
            try:
                result1 = re.findall(r'<ul class="parameter2 p-parameter-list">(.*?)</ul>.*?<p class="more-par">', html, re.S)[
                    0]
                result2 = re.findall('>(.*?)<', result1)
                introduction = {}
                for param in result2:
                    if '：' in param:
                        p1 = param.split('：')
                        introduction[p1[0]] = p1[1]
            except:
                introduction = {}
            # 规格与包装
            try:
                result3 = re.findall(r'<div class="Ptable-item">(.*?)<div class="package-list">', html, re.S)[0]
                result4 = re.findall('<dt>(.*?)</dd>', result3)
                Packaging = {}
                for param in result4:
                    if '</dt><dd>' in param:
                        p1 = param.split('</dt><dd>')
                        Packaging[p1[0]] = p1[1]
            except:
                Packaging = {}
            # 各种评价数量
            urlLeft1 = 'https://club.jd.com/comment/productCommentSummaries.action?referenceIds='
            urlRight1 = '&callback=jQuery600824&_=1534812709081'
            url = urlLeft1 + ProductCode + urlRight1
            html1 = requests.get(url,proxies={'http':ip},headers=headers)
            data1 = json.loads(html1.text[31:-4])
            evaluations = {}
            evaluations["GoodRate"] = data1["GoodRate"]
            evaluations["CommentCountStr"] = data1["CommentCountStr"]
            evaluations["AfterCountStr"] = data1["AfterCountStr"]
            evaluations["GoodCountStr"] = data1["GoodCountStr"]
            evaluations["GeneralCountStr"] = data1["GeneralCountStr"]
            evaluations["PoorCountStr"] = data1["PoorCountStr"]
            # 价格
            urlLeft = 'https://p.3.cn/prices/mgets?callback=jQuery8554643&type=1&area=24_2144_21037_21082&pdtk=&pduid=460357822&pdpin=&pin=null&pdbp=0&skuIds=J_'
            urlRight = '&ext=11100000&source=item-pc'
            url1 = urlLeft + ProductCode + urlRight
            for i in range(3):
                try:
                    html2 = requests.get(url1,proxies={'http':ip},headers=headers)
                    x = json.loads(html2.text[15:-4])
                    price = x["p"]
                except:
                    price = '无'
            fff.write(str(ProductCode)+' '+str(ProductName)+' '+str(price)+' '+str(Packaging)+' '+str(introduction)+' '+str(evaluations)+' '+str(BigType)+' '+str(SmallType1)+'\n')


def GetJdDatacomment(ip):
    url=oriurl
    r = requests.get(url,proxies={'http':ip},headers=headers)
    npage = re.findall('<b>.*?</b><em>/</em><i>(.*?)</i>', r.text, re.S)[0]
    ###判断地址是否为奇数型页码，“%”为奇数型页码，没有为顺序型
    if '%' in url:
        for j in range(int(npage)*2):
            if j%2==1:
                GetComment(url, j, ip)
    else:
        for j in range(int(npage)):
            GetComment(url, j,ip)


def GetJdDatacontent(BigType, SmallType, ip):
    url=oriurl
    r = requests.get(url,proxies={'http':ip},headers=headers)
    npage = re.findall('<b>.*?</b><em>/</em><i>(.*?)</i>', r.text, re.S)[0]
    print(npage)
    ###判断地址是否为奇数型页码，“%”为奇数型页码，没有为顺序型
    if '%' in url:
        for j in range(int(npage)*2):
            if j%2==1:
                GetContent(url,j,BigType,SmallType,ip)
    else:
        for j in range(int(npage)):
            GetContent(url,j,BigType,SmallType,ip)

while 1:
    try:
        print('正在爬取--京东content')
        GetJdDatacontent('蜂蜜', '蜂蜜', ip)
    except:
            print('正在爬取--京东comment')
            GetJdDatacomment(ip)


