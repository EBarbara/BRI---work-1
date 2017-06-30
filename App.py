# -*- coding: utf-8 -*-
"""
Created on Fri Jun 30 08:56:24 2017

@author: Estevan
"""
import logging
import time
import configparser
from MultiOrderedDict import MultiOrderedDict
from InvertedListGenerator import InvertedListGenerator

class App(object):
    
    def __init__(self):
        self.logger = self.startLogging()
        self.startInvertedListModule()
    
    def startLogging(self):
        logger = logging.getLogger('App')
        logHandler = logging.FileHandler('logs/BRI_1.log')
        formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
        logHandler.setFormatter(formatter)
        logger.addHandler(logHandler)
        logger.setLevel(logging.INFO)
        return logger
    
    def logExecutionTime(self, title, startTime):
        finishTime = time.time()
        self.logger.info(("Finish %s: %fs") % (title, finishTime - startTime))
    
    def startInvertedListModule(self):
        startTime = time.time()
        config = self.loadConfig('config/gli.cfg')
        invertedListGenerator = InvertedListGenerator(config, self.logger)
        #invertedListGenerator.execute()
        self.logExecutionTime('Inverted Index Module', startTime)
    
    def loadConfig(self, file):
        self.logger.info('Loading configuration file: ' + file)
        config = configparser.ConfigParser(dict_type=MultiOrderedDict,strict=False)
        config.read(file)
        return config
    
    def execute(self):
        self.logger.info('Starting App')
        
app = App()
app.execute()