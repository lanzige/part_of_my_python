import urllib.robotparser

'''
github_test
qweqwe123
'''
rp=urllib.robotparser.RobotFileParser()
rp.set_url("https://www.taobao.com/robots.txt")
rp.read()
url="https://item.taobao.com/item.htm?spm=a21ct.8141403.0.0.ac1dad8DJ3XTU&scm=1007.12144.83516.8750_4744&pvid=724ac649-0441-464c-a398-c306cb0f374e&id=557005212449"
user_agent='Googlebot'
print(rp.can_fetch(user_agent,url))