# -*- coding: utf-8 -*-

from .Atcstack import Atcstack
from .GShtmltranser import GShtmltranser
import os

filepath = os.path.split(__file__)[0]
filepath = os.path.split(filepath)[0]

def LocalParsing():
    atcs = Atcstack()  
    for cluster in os.listdir(filepath+r'\citation_htmls'):
        for html in os.listdir(filepath+r'\citation_htmls\%s' % cluster):            
            with open(filepath+r'\citation_htmls\%s\%s'%(cluster,html), 'r', encoding='utf-8') as f:
                print('posscessing in:'+r'\citation_htmls\%s\%s'%(cluster,html))
                res= f.read()
                CTGS = GShtmltranser(res,atcs,cluster)
                
            CTGS.attrparser()
    atcs.atcs2csv()
    atcs.cre2csv()
    atcs.atcs2gep()
