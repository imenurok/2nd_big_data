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

#times = 1 #labelをtimes倍にして少数第一位を四捨五入する

def no2array(length,no):
    new_array=[0]*length
    new_array[no]=1
    return new_array
def nosize2array(length,no,size):
    new_array=[0]*length
    new_array[no]=size
    return new_array

def pid_dict_handling():
    
    #dictionary
    pid_dict={}
    category_dict={"ナチュラルローソン菓子":0,"おやつごろシリーズ菓子":1}
    package_dict={"カップ":0,"袋":1,"箱":2}
    genre_dict={"スナック菓子":0,"菓子":1,"パイ加工品":2,"ポテトチップス":3,"チョコレート菓子":4,"種実加工品":5,"チョコレート":6,"ビスケット":7,"クッキー":8,"クラッカー":9,
                "野菜チップス":10,"ラスク":11,"マシュマロ":12,"有機干し芋":13,"ドーナツ":14,"魚介加工品":15,"焼菓子":16,"油菓子":17,"半生菓子":18,"魚介乾製品":19,"準チョコレート":20,
                "米菓":21,"米菓子":22,"パイ":23}
    size_dict1={"4個":4,"7個":7}
    size_dict2={"6枚":6,"5枚":5}
    size_dict3={"10本":10}
    manufacturer_dict= {"株式会社湖池屋":0,"ハース株式会社":1,"ダイシンフーズ株式会社":2,"森永製菓株式会社":3,"カルビー株式会社":4,"株式会社カレイナ":5,"株式会社ミツヤ":6,"株式会社ロッテ":7,"株式会社東ハト":8,"江崎グリコ株式会社":9,"宝製菓株式会社":10,
                        "株式会社ギンビス":11,"株式会社おやつカンパニー":12,"株式会社エイワ":13,"株式会社壮関":14,"株式会社リボン":15,"株式会社合食":16,"イケダヤ製菓株式会社":17,"リスカ株式会社":18,"株式会社末広製菓":19,"ぼんち株式会社":20,
                        "東京カリント株式会社":21,"久保田製菓有限会社":22,"株式会社北食":23,"旺旺ジャパン株式会社":24,"株式会社正栄デリシィ":25,"ニッポー株式会社":26,"ジャパンフリトレー株式会社":27,"イトウ製菓株式会社":28,"カバヤ食品株式会社":29,"阿部幸製菓株式会社":30,
                        "株式会社オリーヴ":31,"ローヤル製菓株式会社":32,"株式会社天乃屋":33,"株式会社栗山米菓":34,"ホンダ製菓株式会社":35,"株式会社道南冷蔵":36,"株式会社不二家":37,"株式会社村田製菓":38,"株式会社ニッコー":39}
    nutrition20_dict={"17～91":54}
    nutrition21_dict={"0.0～0.2":0.1}
    nutrition23_dict={"1.7～2.7":2.2,"2.6～4.0":3.3}
    
    file = open( base_path+'/product.tsv' , 'r' )
    delimiter_str="\t"
    data = csv.reader(file, delimiter=delimiter_str)
    next(file)
    for s_line in data:
        allergy_list=[]
        nutrition_list=[]
        pid = s_line[0]
        category = category_dict[s_line[1]]
        price = int(s_line[3])
        package_type = no2array(len(package_dict),package_dict[s_line[4]])
        for i in range(7,12):
            allergy = s_line[i]
            if allergy=="":
                allergy = "0"
            allergy_list.append(float(allergy))
        genre = no2array(len(genre_dict),genre_dict[s_line[13]])
        size = s_line[14].rstrip("g")
        size_no=0
        if size in size_dict1:
            size=size_dict1[s_line[14]]
            size_no=1
        elif size in size_dict2:
            size=size_dict2[s_line[14]]
            size_no=2
        elif size in size_dict3:
            size=size_dict3[s_line[14]]
            size_no=3
        size=nosize2array(4,size_no,float(size))
        manufacturer = no2array(len(manufacturer_dict),manufacturer_dict[s_line[15]])
        for i in range(16,37):
            nutrition=s_line[i]
            if nutrition=="":
                nutrition="0"
            if i==20:
                if nutrition in nutrition20_dict:
                    nutrition=nutrition20_dict[nutrition]
            if i==21:
                if nutrition in nutrition21_dict:
                    nutrition=nutrition21_dict[nutrition]
            if i==23:
                if nutrition in nutrition23_dict:
                    nutrition=nutrition23_dict[nutrition]
            if (33<=i and i<=35) == False:
                nutrition_list.append(float(nutrition))#トランス脂肪酸、コレステロール、乳糖を排除。これらはfeature_importance_[n]=0
        #node=[category,price]+package_type+allergy_list+genre+size+manufacturer+nutrition_list
        node=[category,price]+package_type+allergy_list+genre+size+manufacturer+nutrition_list
        pid_dict.update({pid:node})
    
    return pid_dict

def wether_10_years_dict_handling():#2005-2015
    
    #dictionary
    wether_10_years_dict={}
    local_dict={0:"北海道",1:"東北",2:"関東",3:"中部",4:"近畿",5:"中国",6:"九州",7:"四国"}#札幌、仙台、東京、長野、大阪、広島、福岡、松山
    
    file = open( base_path+'/wether.csv' , 'r' )
    delimiter_str=","
    data = csv.reader(file, delimiter=delimiter_str)
    
    for s_line in data:
        mon_dict={}
        mon=int(s_line[0])
        num=2
        for i in range(8):
            for j in range(9):
                if (s_line[num+j*2]==""):
                    s_line[num+j*2]="0"
            local=local_dict[i]
            ave_rain=float(s_line[num])
            ave_sun_time=float(s_line[num+2])
            ave_snow=float(s_line[num+4])
            ave_wind=float(s_line[num+6])
            ave_clowd=float(s_line[num+8])
            ave_snow_day=float(s_line[num+10])
            ave_thunder=float(s_line[num+12])
            ave_fog=float(s_line[num+14])
            ave_temp=float(s_line[num+16])
            num+=18
            node=[ave_rain,ave_sun_time,ave_snow]+[ave_wind,ave_clowd,ave_snow_day,ave_thunder,ave_fog,ave_temp]
            #node=[ave_sun_time]+[ave_wind,ave_clowd,ave_fog]
            mon_dict.update({local:node})
        wether_10_years_dict.update({mon:mon_dict})
    return wether_10_years_dict

pid_dict=pid_dict_handling()
wether_10_years_dict=wether_10_years_dict_handling()

def data_handling(line,train=True):
    
    default_no=0
    if train==False:
        default_no=1
    
    #dictionary
    
    area_dict={"関東":0,"近畿":1,"東北":2,"四国":3,"北海道":4,"九州":5,"中部":6,"中国":7}
    location_dict={"ビジネス立地":0,"住宅立地":1,"学校立地":2,"観光立地":3}
    pay_dict={"北海道":391,"東北":403,"九州":394,"近畿":410,"四国":421,"中国":410,"関東":461,"中部":414}#https://doda.jp/guide/heikin/2015/area/
    lowestpay_dict={"北海道":764,"東北":702,"九州":700,"近畿":782,"四国":701,"中国":725,"関東":812,"中部":756}#平成27年度地域別最低賃金改定状況
    
    s_line=line[:-1].split('\t')#タブ区切りファイルをリストに
    pid = s_line[default_no+0]
    date = s_line[default_no+1]
    area = s_line[default_no+2]
    location = s_line[default_no+3]
    natural_lawson_store = s_line[default_no+4]
    
    if train:
        label = s_line[5]
    
    #node
    
    #i_pid = int(pid.lstrip("p")) # "p000" to "000"
    
    i_date = int(date)
    if i_date<201600:
        i_date = int(date)-201506
        i_year = 2015
        i_month = int(date)-201500
    else:
        i_date = int(date)-201600+6
        i_year = 2016
        i_month = int(date)-201600
    i_area = area_dict[area]
    i_location = location_dict[location]
    i_natural_lawson_store = int(natural_lawson_store)
    
    #node=[i_pid,i_date,i_area,i_location,i_natural_lawson_store]
    #node=pid_dict[pid]+[i_month,i_year]+no2array(len(area_dict),i_area)+no2array(len(location_dict),i_location)+[i_natural_lawson_store]#+[pay_dict[area]]+[lowestpay_dict[area]]
    #node=pid_dict[pid]+[i_date]+no2array(len(area_dict),i_area)+no2array(len(location_dict),i_location)+[i_natural_lawson_store]+[pay_dict[area]]+[lowestpay_dict[area]]
    kisetu=0
    if i_date<3:
        kisetsu=1
    elif i_date<6:
        kisetsu=2
    elif i_date<9:
        kisetsu=3
    elif i_date<12:
        kisetsu=0
    else:
        kisetsu=1
    node=pid_dict[pid]+[i_date]+no2array(len(area_dict),i_area)+no2array(len(location_dict),i_location)+[i_natural_lawson_store]+[pay_dict[area]]+[lowestpay_dict[area]]+no2array(4,kisetsu)+[i_year]+wether_10_years_dict[i_month][area] #pay+lowpay XGBturing=0.1752  pay+lowpay+kisetsu 0.1752 #pay+lowpay+kisetsu+year 0.1738 #pay+lowpay+year 0.1771
    #label
    if train:
        #class_label = int(round(float(label),int(math.log10(times)))*times) # *times and round it to the nearest 1
        class_label = float(label)
    #print (str(node)+" , "+str(class_label))
    
    if train:
        return node,class_label
    return node

def main_data_read():
    training_data = []
    training_label = []
    predict_data = []

    file = open( base_path+"/train.tsv", "r" )
    next(file)
    for line in file:
        node,label=data_handling(line,train=True)
        training_data.append( node )
        training_label.append( label )
    file = open( base_path+"/test.tsv" , "r" )
    next(file)
    for line in file:
        node=data_handling(line,train=False)
        predict_data.append( node )
    training_data = np.asarray(training_data)
    training_label = np.asarray(training_label)
    predict_data = np.asarray(predict_data)
    return training_data,training_label,predict_data

def test_data_read(check_date=11):
    training_data = []
    training_label = []
    predict_data = []
    predict_label = []

    file = open( base_path+"/train.tsv", "r" )
    next(file)
    for line in file:
        node,label=data_handling(line,train=True)
        if node[96]!=check_date:
            training_data.append( node )
            training_label.append( label )
        else:
            predict_data.append( node )
            predict_label.append( label )
    training_data = np.asarray(training_data)
    training_label = np.asarray(training_label)
    predict_data = np.asarray(predict_data)
    predict_label = np.asarray(predict_label)
    return training_data,training_label,predict_data,predict_label

def main_feature_name():
    names=[]
    names.append("category")
    names.append("price")
    for i in range(3):
        names.append("package"+str(i))
    for i in range(5):
        names.append("allergy"+str(i))
    for i in range(24):
        names.append("genre"+str(i))
    for i in range(4):
        names.append("size"+str(i))
    for i in range(40):
        names.append("manu"+str(i))
    for i in range(18):
        names.append("nutri"+str(i))#数字は対応してないので注意
    names.append("date")
    for i in range(8):
        names.append("area"+str(i))
    for i in range(4):
        names.append("loca"+str(i))
    names.append("store")
    names.append("pay")
    names.append("lowpay")
    for i in range(4):
        names.append("kisetsu"+str(i))
    names.append("year")
    names.append("rain")
    names.append("sun")
    names.append("snow")
    names.append("wind")
    names.append("clowd")
    names.append("snowday")
    names.append("thunder")
    names.append("fog")
    names.append("temp")
    return names

def pid_check(data_):
    pids=[]
    no=0
    rem_no=(np.zeros(96))
    for line in data_:
        node=np.asarray(line)
        node_check=False
        for i in range(96):
            if node[i]!=rem_no[i]:
                node_check=True
        if node_check:
            rem_no=node[0:96]
            pids.append(no)
        no+=1
    return pids

def submit_data_read(name):
    submit_data = []
    file = open( base_path+"/"+name+".csv" , "r" )
    for line in file:
        s_line = line.strip().split(",")
        submit_data.append( s_line[1] )
    submit_data = np.asarray(submit_data)
    return submit_data

def data_append(name,training_data,predict_data):
    output = submit_data_read(name+"train")
    training_data = np.c_[np.asarray(training_data),np.c_[np.asarray(output)]]
    output = submit_data_read(name+"test")
    predict_data = np.c_[np.asarray(predict_data),np.c_[np.asarray(output)]]
    return training_data,predict_data

def submit_tSNE_read(name):
    submit_data = []
    file = open( base_path+"/"+name+".csv" , "r" )
    for line in file:
        s_line = line.strip().split(",")
        submit_data.append(s_line[1].strip('[').strip(']').split())
    submit_data = np.asarray(submit_data)
    return submit_data

def tSNE_append(name,training_data,predict_data):
    output = submit_tSNE_read(name+"train")
    training_data = np.c_[np.asarray(training_data),np.c_[np.asarray(output)]]
    output = submit_tSNE_read(name+"test")
    predict_data = np.c_[np.asarray(predict_data),np.c_[np.asarray(output)]]
    return training_data,predict_data