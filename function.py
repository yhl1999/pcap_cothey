import os
import re
from threading import current_thread
import config
import random
import bs4
import requests
import zipfile
from urllib.parse import urljoin

#判断目标字串中是否包含给定串，若包含，返回最先出现的串，若不包含，返回None
def re_(link_str):
    pattern = config.pattern
    res = None
    idx_res = len(link_str)
    for p in pattern:
        ad = link_str.find(p)
        if ad == -1:
            pass
        else:
            if ad<idx_res:
                idx_res = ad
                res = p
    return res

#爬取年份网页,根据规则过滤，返回标签文本内容符合规则的对应类以及对应的href所组成的列表
def web_links_cothey(index_url):
    res = requests.get(index_url)
    soup = bs4.BeautifulSoup(res.text,"lxml")
    soup = soup.find('div',attrs={'class': "content"})
    ul_list = soup.findAll('ul')
    links = []
    for ul in ul_list:
        for a in ul.findAll('a',attrs={'class': "main_menu"}):
            context = a.text
            context = context.lower() #转化为小写字母
            href = a.get('href')
            href = urljoin(index_url,href) #将爬取到的相对路径转换为绝对路径
            #print(context, href)
            mal_class = re_(context)

            if mal_class != None:
                links.append([mal_class,href])
            else:
                continue
    print(len(links))
    return links

#爬取包含pcap页面的链接，返回pcap文件的链接
def pcap_href_cothey(web_pcap_url):
    print("--pcap_href_cothey:")
    try:
        res = requests.get(web_pcap_url)
        soup = bs4.BeautifulSoup(res.text, "lxml")
        links = []
        ul = soup.find('ul')
        for a in ul.findAll('a'):
            #print(a.get('href'))
            if (".zip" in a.get('href')) and (("pcap" in a.get('href')) or ("traffic" in a.get('href'))):
                href = urljoin(web_pcap_url, a.get('href'))
                links.append(href)

        for bq in soup.findAll('blockquote'):
            if ".pcap" in bq.text:
                #print(bq.text)
                ul = bq.previous_sibling
                a = ul.find('a')
                href = urljoin(web_pcap_url,a.get('href'))
                #print(href)
                links.append(href)
        print("links:",links)
    except Exception as e :
        print(e)
    return list(set(links))

#根据pcap文件链接，下载指定的pcap文件并解压到对应的路径中
def pcap_download(pcap_url,path):
    print("--pcap_download:")
    zipb = requests.get(pcap_url)
    print(pcap_url)
    zip_path = f"./zip/{current_thread().getName()}.zip"
    f = open(zip_path,"wb")
    f.write(zipb.content)
    f.close()
    with zipfile.ZipFile(file=zip_path,mode="r") as pcap:
        print("namelist:",pcap.namelist())
        for name in pcap.namelist():
            if '.pcap' not in name:
                return False
        pcap.extractall(path,pwd=config.pwd.encode())
    os.remove(zip_path)
    return True

def randquit():
    r = random.randint(0,20)
    if r == 10:
        return True
    else:
        return False

def status_change(iter,value):
    iter = value

def thread_download(pcap_url,href,save_path,i):
    if len(pcap_url) == 0:
        print("pcap_url None")
        print(href)
    else:
        try:
            flag = True
            for url in pcap_url:
                if pcap_download(url, save_path) == False:
                    flag = False
            if flag == True:
                i[2] = 1
        except Exception as e:
            print("download failed")
            print(e)
            print(href)
#web_links_cothey("https://www.malware-traffic-analysis.net/2017/index.html")
#pcap_href_cothey("https://www.malware-traffic-analysis.net/2017/12/29/index.html")
#pcap_download("https://www.malware-traffic-analysis.net/2017/12/29/2017-12-27-thru-29-Necurs-Botnet-malspam-traffic.zip","./pcap/a/")
