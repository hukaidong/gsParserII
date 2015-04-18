# Google Scholar 连接器
# Sessiondef 创建用于连接gs的 session
# GSlinker用于连接GS并返回文本结果
# 先创建通过cites和starts得到引用的结果
# 和将bibtex返回并存储的结果

import requests,time,logging
from bs4 import BeautifulSoup

logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
                    datefmt='%a, %d %b %Y %H:%M:%S')
    
class Sessiondef:
    '''
    给出一个定义好的针对Google Scholar的requests对话
    '''
    Global_Provisional_Header = {'Accept':r'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
                                 'User-Agent':r'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2272.101 Safari/537.36'}
    
    def setting_website_req(self,s):
        '''
        先与GS连通,done
        '''
        logging.debug('访问https://scholar.google.com/')
        gs = s.get(r'https://scholar.google.com/')
        logging.debug('回复' + gs.text[:100])
        with open('sgc.html','w') as f:
                f.write(gs.text)
        time.sleep(1)
        logging.debug('访问scholar_settings')
        GS_Setting_Q = r'https://scholar.google.com/scholar_settings'
        GS_Setting_Query = {'sciifh':'1','hl':'en','as_sdt':'0,5'}
        gs = s.get(GS_Setting_Q,params=GS_Setting_Query)
        logging.debug('回复' + gs.text[:100])
        with open('sgcs.html','w') as f:
                f.write(gs.text)
        time.sleep(1)
        return gs

    def setting_website_parser(self,s):
        '''
        调出GS中的bibtex选项
        '''
        setting_req_bt = self.setting_website_req(s)
        GS_Setting_P = r"https://scholar.google.com/scholar_setprefs"
        GS_Setting_Pre = {'sciifh' : '1',
                          'scisig' : None,
                          'inststart' : '0',
                          'as_sdt' : '0,5',
                          'as_sdtp' : '',
                          'num' : '20',
                          'newwindow' : '1',
                          'scis' : 'yes',
                          'scisf' : '4',                          
                          'hl' : 'en',
                          'lang' : 'all',
                          'instq' :'',
                          'inst' : None}
        soup = BeautifulSoup(setting_req_bt.text)
        scifig = soup.find(name='form', attrs={'id': 'gs_settings_form'})
        if scifig is None:
            logging.error('info', 'parsing settings failed: no form')
        scifig = scifig.find('input', attrs={'type':'hidden', 'name':'scisig'})
        if scifig is None:
            logging.error('info', 'parsing settings failed: scisig')
        inst = soup.find(name='input',  attrs={'name': 'inst'})
        if inst is None:
            logging.error('info', 'parsing settings failed: no inst')            
        urlargs = {'scisig' : scifig['value'],
                   'inst' : inst['value']}
        GS_Setting_Pre.update(urlargs)
        logging.debug('调出Bibtex')
        gs = s.get(GS_Setting_P, params = GS_Setting_Pre)
        logging.debug(gs.url+'回复：'+gs.text[:100])
        logging.debug(gs.headers)
        with open('sgcss.html','w') as f:
                f.write(gs.text)
        return s            
                                  
    def reinit_session(self ):
        '''
        创建一个GS会话,并用setting_website_parser初始化会话
        '''
##        GAE_Global_Proxy = {'https':'127.0.0.1:8087'}
        GAE_Global_Proxy = None
        logging.debug('GS会话创建中')
        s = requests.Session()
        s.headers = self.Global_Provisional_Header
        s.proxies  = GAE_Global_Proxy
        logging.debug('GS会话创建完成')
        s = self.setting_website_parser(s)
        return s

    def ses(self):
        return self.s

    def __init__(self):
        self.s = self.reinit_session()
    
    


