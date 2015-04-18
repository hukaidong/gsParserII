
from .Atcstack import Atcstack
from .Sessiondef import Sessiondef
from .ScholarUtils import ScholarUtils
from .GSLinker import GSLinker
from .GShtmltranser import GShtmltranser
from .ScholarArticle import ScholarArticle
from .LocalParsing import LocalParsing

import logging

logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
                    datefmt='%a, %d %b %Y %H:%M:%S')
