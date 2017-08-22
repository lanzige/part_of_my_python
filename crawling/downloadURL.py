import urllib.request
import urllib.error
import re
import urllib.parse
import time
import urllib.robotparser

def download(url,user_agent="wswp",num=3):
    '''
    下载url页面，附带一个报文头，出错自动尝试重复下载3次
    :param url:要下载的地址
    :param user_agent:报文头
    :param num:失败尝试重复下载次数
    :return:返回下载的页面代码
    '''
    print("try download:"+str(url))
    headers={"User-agent":user_agent}
    req=urllib.request.Request(url,headers=headers)
    try:
        html=urllib.request.urlopen(req).read().decode()
    except urllib.error.URLError as e:
        print("download error:%s"%(e.reason))
        html=None
        #判断是HTTPError还是URLError
        if hasattr(e,"code"):
            print("e.code is %s"%(e.code))
        if hasattr(e,"reason"):
            print("this is URLError...")
        #下载网页出问题，重复尝试下载num次
        if num>0:
            print("download %d times."%(num))
            if hasattr(e,'reason') or hasattr(e,"code"):
                return download(url,num=num-1)

    return html

def link_crawler(seed_url,link_regex):

    '''
    传进来的网址作为初始值下载所有连接
    :param seed_url: 初始url
    :param link_regex:
    :return:返回查询到的链接
    '''
    rp=get_robots(seed_url)
    craw_quene=[seed_url]
    seen=set(craw_quene)
    while craw_quene:
        url=craw_quene.pop()
        html=download(url)
        if rp is not None:
            if not rp.can_fetch("wswp",url):
                print("you can't download this web page...")
                continue
        if html is None:
            print("html is None...")
            continue
        for link in get_links(html):
            if re.match(link_regex,link):
                link=urllib.parse.urljoin(seed_url,link)
                if link not in seen:
                    craw_quene.append(link)
                    seen.add(link)
    return seen

def get_links(html):

    '''
    获取网页中符合条件的所有连接地址存储在列表中。
    :param html: 网页代码
    :return: 所有的链接
    '''
    webpage_regex=re.compile('<a[^>]+href=["\'](.*?)["\']',re.IGNORECASE)
    return webpage_regex.findall(html)

def get_robots(url):
    robots_url=urllib.parse.urljoin(url,'/robots.txt')
    rp=urllib.robotparser.RobotFileParser()
    rp.set_url(robots_url)
    rp.read()
    if rp.allow_all:
        print("allow all visit...")
    if rp.disallow_all:
        print("disallow all visit")
    return rp


if __name__=="__main__":
    url="http://www.acfun.cn/"
    reg='/[A-Za-z]/.*'
    page_links=link_crawler(url,reg)
    for link in page_links:
        print(link)
        time.sleep(2)
