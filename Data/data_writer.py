#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import division

import re
import math
import csv
import numpy as np

import os
base_path=os.path.dirname(os.path.abspath(__file__))

np.random.seed(0)

def submit_data_write(name,data,silent):
    file = open( base_path+"/"+name+".csv" , "w")
    id=0
    for line in data:
        if silent==False:
            print(str(id)+","+str(line))
        file.write(str(id)+","+str(line)+"\n")
        id+=1
def data_write(name,train_data,test_data,silent=False):
    submit_data_write(name+"train",train_data,silent=True)
    submit_data_write(name+"test",test_data,silent)