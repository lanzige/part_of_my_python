# coding=utf-8
import urllib.request
import re
import urllib.error
import random
import bs4
import threading

def get_UserAgent():
    '''
    获取可用的user-agent
    :return:
    '''
    Android_agent=["Mozilla/5.0 (Linux; Android 4.1.1; Nexus 7 Build/JRO03D) AppleWebKit/535.19 (KHTML, like Gecko) Chrome/18.0.1025.166 Safari/535.19",
                   "Mozilla/5.0 (Linux; U; Android 4.0.4; en-gb; GT-I9300 Build/IMM76D) AppleWebKit/534.30 (KHTML, like Gecko) Version/4.0 Mobile Safari/534.30",
                   "Mozilla/5.0 (Linux; U; Android 2.2; en-gb; GT-P1000 Build/FROYO) AppleWebKit/533.1 (KHTML, like Gecko) Version/4.0 Mobile Safari/533.1"]

    Firefox_agent=["Mozilla/5.0 (Windows NT 6.2; WOW64; rv:21.0) Gecko/20100101 Firefox/21.0",
                   "Mozilla/5.0 (Android; Mobile; rv:14.0) Gecko/14.0 Firefox/14.0"]

    Chrome_agent=["Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/27.0.1453.94 Safari/537.36"
                  "Mozilla/5.0 (Linux; Android 4.0.4; Galaxy Nexus Build/IMM76B) AppleWebKit/535.19 (KHTML, like Gecko) Chrome/18.0.1025.133 Mobile Safari/535.19"]

    IOS_agent=["Mozilla/5.0 (iPad; CPU OS 5_0 like Mac OS X) AppleWebKit/534.46 (KHTML, like Gecko) Version/5.1 Mobile/9A334 Safari/7534.48.3"
               "Mozilla/5.0 (iPod; U; CPU like Mac OS X; en) AppleWebKit/420.1 (KHTML, like Gecko) Version/3.0 Mobile/3A101a Safari/419.3"]

    User_agents=[Android_agent,Firefox_agent,Chrome_agent,IOS_agent]

    row=random.randint(0,len(User_agents)-1)
    col=random.randint(0,len(User_agents[row])-1)

    return User_agents[row][col]

def get_ip(html,ip_reg='\"origin\": \"(.*?)\"'):
    '''
    获得本地ip地址
    :param headers:
    :return:
    '''
    # url="http://1212.ip138.com/ic.asp"
    # req=urllib.request.Request(url,headers=headers)
    # try:
    #     response=urllib.request.urlopen(req)
    #     html=response.read().decode("gbk")
    # except urllib.error.URLError as e:
    #     print("download error:%s"%(e.reason))
    #     html=None
    if html is not None:
        html=html.decode("gbk")
        ip_re=re.compile(ip_reg)
        ip=ip_re.findall(html)
    else:
        ip=None

    return ip

def get_ProxyIP(html):
    '''
    获得代理的IP地址和端口号
    :return:
    '''
    # url="http://www.xicidaili.com/nn/"
    # IPs=[]
    # agent=get_UserAgent()
    # headers={"User-Agent":agent}
    # req=urllib.request.Request(url,headers=headers)
    # try:
    #     page=urllib.request.urlopen(req)
    #     html=page.read()
    # except urllib.error.URLError as e:
    #     print("download errer:%s"%(e.reason))
    IPs=[]
    bsObject=bs4.BeautifulSoup(html,"html.parser")
    tr=bsObject.find_all("tr",attrs={"class":["odd",""]})
    for item in tr:
        tds=item.find_all("td")[1:6]
        Ip_Port=tds[0].get_text()+":"+tds[1].get_text()
        Proxy_class=tds[4].get_text().lower()
        IPs.append({Proxy_class:Ip_Port})

    return IPs

def get_html(url):
    agent=get_UserAgent()
    headers={"User-Agent":agent}
    req=urllib.request.Request(url,headers=headers)
    try:
        response=urllib.request.urlopen(req)
        html=response.read()
    except urllib.error.URLError as e:
        print("download error:%s"%(e.reason))
        html=None

    return html


def test_ip():
    proxy_url="http://www.xicidaili.com/wt/"
    ip_url="http://httpbin.org/ip"

    #获得代理资源
    proxy_html=get_html(proxy_url)
    proxy_ips=get_ProxyIP(proxy_html)

    #创建代理处理器
    proxy=proxy_ips[random.randint(0,len(proxy_ips)-1)]

    proxy_support=urllib.request.ProxyHandler(proxy)
    opener=urllib.request.build_opener(proxy_support)
    opener.addheaders=[("User-Agent",get_UserAgent())]

    #用代理处理器获得ip页面
    try:
        response=opener.open(ip_url)
        html=response.read()
        ip=get_ip(html)
        print("now test_ip is:%s and return_ip is:%s"%(proxy,ip))
    except urllib.error.URLError as e:
        print("The Error is:%s"%(e.reason))
    #print("now proxy_ip is:%s"%(ip))
    #return ip


if __name__=="__main__":
    ths=[]
    print('---START---')
    for i in range(10):
        th=threading.Thread(target=test_ip)
        th.start()
        ths.append(th)

    for item in ths:
        item.join()

    print('---END---')