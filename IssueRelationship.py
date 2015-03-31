## coding : utf-8 ##
## author : ccdd  ##

import re
from http import cookiejar
from bs4 import BeautifulSoup as Bs
from urllib import request,parse
from os import path

# global states might developed later
current_content = path.split(path.realpath(__file__))[0]
Gsweb = r'https://scholar.google.com/scholar'
goagent_Available = False

# global opener defination with goagent
proxy = request.ProxyHandler({'https':r'127.0.0.1:8087'})
cj = cookiejar.CookieJar()
if goagent_Available == True :
    browser = request.build_opener(proxy,request.HTTPCookieProcessor(cj))
else:
    browser = request.build_opener(request.HTTPCookieProcessor(cj))
browser.add_headers = (r'User-agent', r'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2272.104 Safari/537.36',\
                        'Accept',r'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8')

def downloadCitation(cite_req):
    data = parse.urlencode({'cites':cite_req}).encode('utf-8')
    print (data)
    citation = browser.open(Gsweb,data)
##    try:
##        citation = browser.open(Gsweb+'?'+data)
##    except:
##        print ('Error : connective error, using local example insteadly')
##        with open(current_content+r'/example.html', 'rb') as example_renew:
##            citation = example_renew.read(0)
    with open(current_content+r'/example.html', 'wb') as example_renew:
        example_renew.write(citation.read())
    print (citation.read().decode('utf-8'))


if __name__ == '__main__':
    with open(current_content+r'/requirement.txt', 'r') as cite_req_file:
        cite_reqs = cite_req_file.readlines()
    for cite_req in cite_reqs:
        downloadCitation(cite_req)
        
