# Google Scholar 连接器
# GSlinker用于连接GS并返回文本结果

import requests,time,logging,os
from .GShtmltranser import GShtmltranser
from bs4 import BeautifulSoup
from .Sessiondef import Sessiondef

from .Atcstack import Atcstack

logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
                    datefmt='%a, %d %b %Y %H:%M:%S')

filepath = os.path.split(__file__)[0]
filepath = os.path.split(filepath)[0]

class GSLinker:
    '''
    每给出一个Google Scholar地址，返回其二进制数据内容
    '''
    def __init__(self):
        self.url = r'https://scholar.google.com/scholar'
        self.params = {'cites':'0',
                       'as_sdt':'2005',
                       'sciodt':'0,5',
                       'hl':'en',
                       'scipsc':'',
                       'start':None,
                       'num':'20',
                        }
        sdf = Sessiondef()
        self.s = sdf.ses()
        self.resource = ''
        self.resources = []

    def GSlink(self):
        self.re = self.s.get(self.url, params=self.params)
        self.s.headers.update(referer = self.re.url)
        self.resource = self.re.text

    def GSQureybyCluster(self, cluster):
        self.params.update(cites=cluster)
        self.GSlink()
        Gst = GShtmltranser(self.resource,Atcstack(),cluster)                       
        self.citeamount = Gst.citeamount()
        self.resources.append(self.resource)        
        self.params['start'] = 20
        while (self.params['start']< self.citeamount):
            time.sleep(60)
            try:
                self.GSlink()            
            except:
                self.GSlink()
            self.resources.append(self.resource)
            self.params['start'] += 20
        return self.resources
    
    def GSQuery(self,cluster):
        fp = filepath + '\citation_htmls\\' +str (cluster)
        if not os.path.exists(fp): os.mkdir(fp) 
        self.GSQureybyCluster(cluster)
        for num , resource in enumerate(self.resources):
            with open(fp +'\%s.html' % str(num+1),'w') as f:
                f.write(resource)
        
        
        
        

              
                       
        
    


            
