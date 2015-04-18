#储存从GS上取得每个条目的信息

class ScholarArticle(object):
    def __init__(self):
        # The triplets for each keyword correspond to (1) the actual
        # value, (2) a user-suitable label for the item, and (3) an
        # ordering index:
        self.attrs = {  'title' : None }
        # The citation data in one of the standard export formats,
        # e.g. BibTeX.
        self.citation_data = None

    def atc2dict(self):
        allinfo = self.attrs
        allinfo.update({'cluster':self.citation_data})
        return allinfo
    
