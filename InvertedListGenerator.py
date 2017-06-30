# -*- coding: utf-8 -*-
"""
Created on Sun Jun 25 16:09:05 2017

@author: Estevan
"""
from lxml import etree

class InvertedListGenerator(object):
    def __init__(self, config, logger):
        super(InvertedListGenerator, self).__init__()
        self.logger = logger
        print(config.get('configuration', 'LEIA'))
        self.read = config.get('configuration', 'LEIA')
        self.write = config.get('configuration', 'ESCREVA')[0]
        self.documents = {}
        self.invertedIndex = {}
        
    def execute(self):
        self.logger.info("Starting Inverted List Generator Module")
        if self.read:
            print(self.read)
        else:
            self.logger.error("InvertedListGenerator: No input file found")
        
    def read_data(self, input_file):
        parser = etree.XMLParser(dtd_validation=True)
        file = etree.parse(input_file, parser)
        
        for record in file.getroot().iterchildren():
            for element in record.iterchildren():
                if(element.tag == 'RECORDNUM'):
                    print(element.tag, element.text)
                if(element.tag == 'ABSTRACT'):
                    print(element.tag, element.text)
                elif(element.tag == 'EXTRACT'):
                    print(element.tag, element.text)
            print("-------------------------------")
        return file
            
#load_config('gli.cfg')
#for input_file in input_files:
#   read_data(input_file)