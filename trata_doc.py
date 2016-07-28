# -*- coding: UTF-8 -*-
# encoding: iso-8859-1
# encoding: win-1252

import string
import re
import xml.etree.ElementTree as ET

#metodo que le o arquivo wikipedia
def leWiki():
    tree = ET.parse('ptwiki-v2.trec')
    root = tree.getroot()
    
    return root
    
    
print "tag inicial:"

print leWiki().tag
    

