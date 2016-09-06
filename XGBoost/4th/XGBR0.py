#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import division

import re
import sys
import math
import csv
import numpy as np
from sklearn.ensemble import RandomForestRegressor,GradientBoostingRegressor,BaggingRegressor,ExtraTreesRegressor,AdaBoostRegressor
from sklearn import grid_search
from sklearn.linear_model import Ridge,Lasso,RidgeCV,LassoCV,LinearRegression,SGDRegressor
from xgboost import XGBRegressor
from sklearn.neighbors import KNeighborsRegressor
from sklearn.tree import DecisionTreeRegressor
from sklearn.svm import SVR
from sklearn.feature_selection import SelectFromModel
from sklearn.manifold import TSNE
from sklearn.decomposition import PCA
from sklearn.cross_validation import KFold,cross_val_score

import xgboost as xgb

import matplotlib.pyplot as plt
plt.style.use('ggplot')

import sys,os
sys.path.append(os.path.dirname(os.path.abspath(__file__)) + '/../../Data')
print os.path.dirname(os.path.abspath(__file__)) + '/../../Data'
folders = str(os.path.dirname(os.path.abspath(__file__))).replace('\\','/').split('/')
folder_name = folders[len(folders)-1]
print folder_name
import data_reader
import data_writer

from sklearn.metrics import make_scorer
def rmsle(actual, pred):
    # Calculates the error, given an array of actual values and predicted values
    squared_errors = (np.log(pred + 1) - np.log(actual + 1)) ** 2
    mean_squared = np.sum(squared_errors) / len(squared_errors)
    return np.sqrt(mean_squared)
scorer = make_scorer(rmsle, greater_is_better=False)

np.random.seed(0)

training_data,training_label,predict_data=data_reader.main_data_read()
names = data_reader.main_feature_name()
training_data=np.delete(training_data,124,1)
predict_data=np.delete(predict_data,124,1)
training_data=np.delete(training_data,118,1)
predict_data=np.delete(predict_data,118,1)
training_data=np.delete(training_data,42,1)
predict_data=np.delete(predict_data,42,1)
names=np.asarray(names).reshape(1,len(names))
names=np.delete(names,124,1)
names=np.delete(names,118,1)
names=np.delete(names,42,1)
names=names.reshape(names.shape[1])
print names.shape,training_data.shape

if len(names) != len(training_data[0]):
    print "names length:"+str(len(names))+" != training_data[0]_length:"+str(len(training_data[0]))
    print "error!"
    sys.exit()

max_depth,min_child_weight,gamma,subsample,colsample_bytree,reg_alpha,learning_rate=(13, 4, 0.0, 0.8, 0.8, 5e-06, 0.002)
model = XGBRegressor(n_estimators=5000,max_depth=max_depth,min_child_weight =min_child_weight,subsample=subsample,colsample_bytree=colsample_bytree,scale_pos_weight = 1,gamma=gamma,reg_alpha=reg_alpha,learning_rate=learning_rate)
pid_list=data_reader.pid_check(training_data)
model.fit(training_data,training_label)
training_output,predict_output = model.predict(training_data),model.predict(predict_data)
data_writer.data_write(folder_name,training_output,predict_output,silent=True)

score = model.booster().get_fscore()
mapper = {'f{0}'.format(i): v for i, v in enumerate(names)}
mapped = {mapper[k]: v for k, v in score.items()}
fig, ax = plt.subplots(1, 1, figsize=(7, 25))
xgb.plot_importance(mapped,ax=ax)
#plt.show()
plt.savefig("graph.png")

all_output=0
rem=[]
for i in range(12):
    training_data,training_label,predict_data,predict_label=data_reader.test_data_read(i)
    training_data=np.delete(training_data,124,1)
    predict_data=np.delete(predict_data,124,1)
    training_data=np.delete(training_data,118,1)
    predict_data=np.delete(predict_data,118,1)
    training_data=np.delete(training_data,42,1)
    predict_data=np.delete(predict_data,42,1)
    model.fit(training_data,training_label)
    training_output,predict_output = model.predict(training_data),model.predict(predict_data)
    #data_writer.data_write("test"+folder_name,training_output,predict_output,silent=True)
    rem.append(np.sqrt(np.mean(np.power(np.log(np.asarray(predict_output)+1)-np.log(np.asarray(predict_label)+1), np.zeros(len(predict_output))+2))))
print np.asarray(rem)
print str(np.mean(np.asarray(rem)))+" + "+str(np.std(np.asarray(rem)))
