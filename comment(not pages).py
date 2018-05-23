import urllib.request
import http.cookiejar
import re
import ssl
# 解决BUG：urllib.error.URLError: <urlopen error [SSL: CERTIFICATE_VERIFY_FAILED] certificate verify failed (_ssl.c:777)>
ssl._create_default_https_context = ssl._create_unverified_context
# 设置视频编号
vid = "1151993549"
# 设置评论起始编号
comid = "1526958330405"
# 构造出真实评论请求网址
url = "https://video.coral.qq.com/varticle/" + vid + "/comment/v2?callback=_varticle" + vid + "commentv2&orinum=10&oriorder=o&pageflag=1&scorecursor=0&orirepnum=2&reporder=o&reppageflag=1&source=9&_=" + comid
# 设置头信息伪装成浏览器爬取
headers = {"Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
                     "Accept-Encoding": "gb2312,utf-8",
                     "Accept-Language": "zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3",
                     "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) Apple WebKit/537.36(KHTML, like Gecko)Chrome/38.0.2125.122 Safari/537.36 SE 2.X MetaSr 1.0",
                     "Connection": "keep-alive",
                     "referer": "qq.com"}
# 设置cookie
cjar = http.cookiejar.CookieJar()
opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(cjar))
headall = []
for key, value in headers.items():
    item = (key, value)
    headall.append(item)
opener.addheaders = headall
urllib.request.install_opener(opener)
# 爬取该网页
data = urllib.request.urlopen(url).read().decode("utf-8")
# 分别构建筛选id、用户名、评论等内容的正则表达式
idpat = '\{"userid":"(.*?)",'     # 网页中一个userid对应2串数字，加入“\{”只查询{"userid":..."nick"中的数据

# 分别根据正则表达式筛选出信息
Info = []
content = []
j = 0
k = 0
idlist = re.compile(idpat, re.S).findall(data)
for id in idlist:
    userpat = '"' + str(id) + '","nick":"(.*?)",'
    userlist = re.compile(userpat, re.S).findall(data)
    Info.append(userlist[0])
    conpat = '"' + str(id) + '","content":"(.*?)",'
    conlist = re.compile(conpat, re.S).findall(data)
    content.append(conlist[0])
    Info[j] = "用户：" + Info[j] + "\n" + "评论：" + content[k]
    if len(conlist) > 1:
        for i in range(1, len(conlist)):
            content.append(conlist[i])
            num = k + i
            Info[j] = Info[j] + "\n" + "评论" + str(i+1) + ":" + content[num]
            k += 1
    j += 1
    k += 1


for i in range(len(Info)):
    print(Info[i])
    # print("用户名：" + eval('u"' + Info[i] + '"'))
    # print("评论：" + eval('u"' + content[i] + '"'))


