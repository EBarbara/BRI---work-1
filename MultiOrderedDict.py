# -*- coding: utf-8 -*-
"""
Created on Fri Jun 30 11:51:23 2017

@author: Estevan
"""
from collections import OrderedDict

class MultiOrderedDict(OrderedDict):
    def __setitem__(self, key, value):
        if isinstance(value, list) and key in self:
            self[key].extend(value)
        else:
            super(OrderedDict, self).__setitem__(key, value)