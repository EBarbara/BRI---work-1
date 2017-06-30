# -*- coding: utf-8 -*-
"""
Created on Fri Jun 30 08:56:24 2017

@author: Estevan
"""
import logging

class App(object):
    
    def __init__(self):
        self.logger = self.initLogger()
    
    def initLogger(self):
        logger = logging.getLogger('App')
        logHandler = logging.FileHandler('logs/BRI_1.log')
        formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
        logHandler.setFormatter(formatter)
        logger.addHandler(logHandler)
        logger.setLevel(logging.INFO)
        return logger
    
    def execute(self):
        self.logger.info('Starting App')
        
app = App()
app.execute()