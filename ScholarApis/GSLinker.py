# Google Scholar 连接器
# GSlinker用于连接GS并返回文本结果

import requests,time,logging
from .GShtmltranser import GShtmltranser
from bs4 import BeautifulSoup
from .Sessiondef import Sessiondef

logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
                    datefmt='%a, %d %b %Y %H:%M:%S')
    
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
                       'num':'20'}
        sdf = Sessiondef()
        self.s = sdf.ses()
        self.resource = ''
        self.resources = []

    def GSlink(self):
        self.resource = self.s.get(self.url, params=self.params)

    def GSQureybyCluster(self, cluster):
        self.params.update(cites=cluster)
        self.GSlink()
        Gst = GShtmltranser(self.resource.text)
        self.citeamount = Gst.citeamount()
        self.resources.append(self.resource.text)
        self.params['start'] = 10
        while (self.params['start']< self.citeamount):
            time.sleep(2)
            self.GSlink()
            self.resources.append(self.resource)
            self.params['start'] += 10
        return self.resources

        

              
                       
        
    


            
