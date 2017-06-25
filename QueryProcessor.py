# -*- coding: utf-8 -*-
"""
Created on Sun Jun 25 08:16:19 2017

@author: Estevan
"""

from lxml import etree

def load_config(config_file):
    with open(config_file) as config:
        global input_file, query_file, result_file
        input_file = config.readline().replace('LEIA=', '').rstrip()
        query_file = config.readline().replace('CONSULTAS=', '').rstrip()
        result_file = config.readline().replace('ESPERADOS=', '').rstrip()
        
def read_queries(input_file):
    parser = etree.XMLParser(dtd_validation=True)
    filequery = etree.parse(input_file, parser)
    
    for query in filequery.getroot().iterchildren("*"):
        for element in query.iterchildren("*"):
            print(element.tag, element.text)
            for subelement in element.iterchildren("*"):
                print(subelement.tag, subelement.attrib, subelement.text)
        print("-------------------------------")

load_config('pc.cfg')
read_queries(input_file)