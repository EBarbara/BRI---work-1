# -*- coding: utf-8 -*-
"""
Created on Sun Jun 25 08:16:19 2017

@author: Estevan
"""

from lxml import etree

parser = etree.XMLParser(dtd_validation=True)
filequery = etree.parse("cfquery.xml", parser)

for query in filequery.getroot().iterchildren("*"):
    for element in query.iterchildren("*"):
        print(element.tag, element.text)
        for subelement in element.iterchildren("*"):
            print(subelement.tag, subelement.attrib, subelement.text)
    print("-------------------------------")