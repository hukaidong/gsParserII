# 翻译各种从GSlinker中得到的html信息

from bs4 import BeautifulSoup
from .ScholarArticle import ScholarArticle
import re,logging


logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
                    datefmt='%a, %d %b %Y %H:%M:%S')

class GShtmltranser(object):
    def __init__(self,resource,atcstack,cluster):
        '''
        resources: 从GS上抓取的html文件，str格式
        '''
        self.soup = BeautifulSoup(resource)
        self.atcstack = atcstack
        self.cluster = cluster


    def citeamount(self):
        soup = self.soup.find(name = 'div', attrs={'id': 'gs_ab','role':'navigation'})
        ctmstr = soup.find(text = re.compile('About \d+ results'))
        return int(re.match(r'About (\d+) results',ctmstr).group(1))

    def attrparser(self):
        soup = self.soup.find(name = 'div', attrs={'id': 'gs_res_bdy'})
        for div in soup.findAll(name = 'div', class_ = 'gs_r'):
            try:
                self._parse_article(div)                
                self._clean_article()
                if self.articl.citation_data:
                    self.handle_article(self.articl)
                elif self.article['title']:
                    logging.warning('No citation information in'+self.article['title']+', ignore')  
            except:
                logging.warning('Attrparser failed with:\n'+div.prettify())   

    def _clean_article(self):
        """
        This gets invoked after we have parsed an article, to do any
        needed cleanup/polishing before we hand off the resulting
        article.
        """
        if self.article['title']:
            self.article['title'] = self.article['title'].strip()
                              
    def _parse_article(self, div):
        self.articl = ScholarArticle()
        self.article = self.articl.attrs

        for tag in div.children:
            try:
                if 'gs_ri' in tag['class'] and tag.h3 and tag.h3.a and tag.h3.a.findAll(text=True):
                    self.article['title']=tag.h3.a.find(text=True)
                    self.article['url'] = tag.h3.a['href']
                    if tag.find(name = 'a', text = re.compile(r'Cited by \d+')) :
                        self.article['url_citation'] = tag.find(name = 'a', text = re.compile(r'Cited by \d+')).attrs['href']
                        self.articl.citation_data = re.search(r'cites=(\d+)',self.article['url_citation']).group(1)
                    elif tag.find(name = 'a', text = re.compile(r'All \d+ versions')):
                        self.article['url_citation'] = None
                        clusterwebsite = tag.find(name = 'a', text = re.compile(r'All \d+ versions')).attrs['href']
                        self.articl.citation_data = re.search(r'cluster=(\d+)',clusterwebsite).group(1)
                    self.article['url_BibTeX'] = tag.find(name = 'a', text = re.compile(r'Import into BibTeX')).attrs['href']
            except:
                logging.warning('parsing faild in:', tag.prettify())

    def handle_article(self,atc):
        self.atcstack.addarticle(atc)
        cluster = self.cluster
        self.atcstack.add_cite_relation(atc,cluster)
