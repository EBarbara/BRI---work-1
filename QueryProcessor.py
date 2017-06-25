# -*- coding: utf-8 -*-
"""
Created on Sun Jun 25 08:16:19 2017

@author: Estevan
"""

import csv
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
    
    for query in filequery.getroot().iterchildren():
        for element in query.iterchildren():
            print(element.tag, element.text)
            for item in element.iterchildren():
                print(item.tag, item.attrib, item.text)
        print("-------------------------------")
    return filequery

def process_queries(queries, query_file):
    with open(query_file, 'w+', newline = '') as csvfile:
        fieldnames = ['query_number', 'query_text']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        
        for query in queries.getroot().iterchildren():
            query_number = ''
            query_text = ''
            for element in query.iterchildren():
                if(element.tag == 'QueryNumber'):
                    query_number = element.text
                elif(element.tag == 'QueryText'):
                    query_text = element.text.replace(';', ',').replace('\n', '').replace('   ', ' ')
            writer.writerow({'query_number': query_number, 'query_text': query_text})
            
def gen_expected(queries, result_file):
    with open(result_file, 'w+', newline = '') as csvfile:
        fieldnames = ['query_number', 'doc_number', 'doc_votes']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        
        for query in queries.getroot().iterchildren():
            query_number = ''
            doc_number = ''
            doc_votes = ''
            for element in query.iterchildren():
                if(element.tag == 'QueryNumber'):
                    query_number = element.text
                elif(element.tag == 'Records'):
                    for item in element.iterchildren():
                        doc_number = item.text
                        doc_votes = item.attrib.get("score")
                        writer.writerow({'query_number': query_number, 'doc_number': doc_number, 'doc_votes': doc_votes})
        
load_config('pc.cfg')
queries = read_queries(input_file)
process_queries(queries, query_file)
gen_expected(queries, result_file)