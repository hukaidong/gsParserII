
import csv,re
from .ScholarArticle import ScholarArticle

path = re.search(r'(.+)ScholarApis\\Atcstack\.py',__file__).group(1)


class Atcstack(object):
    def __init__(self):
        self.articles={}
        self.crelation={}

    def addarticle(self, atc):
        self.articles.update({atc.citation_data:atc})

    def add_cite_relation(self, atc, cluster):   
        if cluster not in self.crelation: 
            self.crelation.update({cluster:[]})
        self.crelation[cluster].append(atc.citation_data)
        
    def atcs2csv(self):
        with open(path + r'storage\articles.csv','w',encoding='utf-8') as csvfile:
            fieldnames = ['cluster', 'title','url','url_citation','url_BibTeX','citation_amount']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            for key in self.articles.keys():
                writer.writerow(self.articles[key].atc2dict())
                
    def cre2csv(self):
        with open(path + r'storage\crelation.csv','w',encoding='utf-8') as csvfile:
            fieldnames = ['Source', 'Target']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            for key in self.crelation.keys():
                for tag in self.crelation[key]:
                    info = {'Source':key,
                            'Target':tag}
                    writer.writerow(info)

    def csv2atcs(self):
        with open(path + r'storage\articles.csv','r',encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                atc = ScholarArticle()
                atc.attrs.update(row)
                atc.citation_data = atc.attrs['cluster']
                self.addarticle(atc)
            
    def atcs2gep(self):
        with open(path + r'storage\articles_gephi.csv','w',encoding='utf-8') as csvfile:
            fieldnames = ['Id', 'Label','url']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            for key in self.articles.keys():
                dicta = self.articles[key].atc2dict()
                gephi = { 'Id': dicta['cluster'],
                          'Label' : dicta['title'],
                          'url': dicta['url']}
                writer.writerow(gephi)
                
