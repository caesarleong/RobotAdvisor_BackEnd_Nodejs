# -*- coding: utf-8 -*-
#!/usr/bin/env python3
"""
Created on Thu Feb 16 11:44:05 2017

@author: user
"""

import time
from numba import jit, autojit,int32,cuda
from CovCorDAO import CovCorDAO

hostname = '140.119.19.108'
username = 'mlstd'
password = 'iloveml'
database = 'mlclass'
port = Í5432

import psycopg2
import numpy as np
from datetime import date,timedelta
from CovCor import CovCor

def GetCorMatrix(FundNames,TheDay,timeinterval):
    myConnection = psycopg2.connect( host=hostname, user=username, password=password, database=database, port=port )
    
    DBAction = CovCorDAO()
    interval = 365 #初始化
    #TheDayStr = str(TheDay)
    CovCorAction = CovCor(TheDay,timeinterval)
    if(CovCorAction.timeinterval=='1Y') :
        interval = 365 #1年的約略天數
    else : interval = 1095 #3年的天數
    
    #fromdate = date(TheDayStr[0:4],TheDayStr[5:7],TheDayStr[8:]) # X:X (included:excluded)
    fromdate = CovCorAction.TheDay
    todate = CovCorAction.TheDay - timedelta(interval) #往前一年的interval   use timedelta to cut 1 year
    enddate = date(2020,12,31)
    daygenerator = (fromdate + timedelta(x + 1) for x in range((fromdate - todate).days))
    daygenerator2 = (fromdate + timedelta(x + 1) for x in range((enddate - fromdate).days))
    #0:星期一  1:星期二 .... 6:星期日
    #因為這個資料庫是從2000~2020年間的工作日區間，共5479天，我要的是夾在中間的一年
    WorkDaysBetween = sum(1 for day in daygenerator if day.weekday() <5) #因為資料庫中只存工作日，所以這邊算區間有多少工作日
    WorkDaysAfter = sum(1 for day in daygenerator2 if day.weekday() <5)
    #print("WorkDays",WorkDaysBetween)
    #print("WorkDaysAfter",WorkDaysAfter)
    
    #DBAction.CreateTable(myConnection)
    #DBAction.DropTable(myConnection)
    
    vals = []
    cutvals = []
    AllTStart = time.time()
    FundNamesStr = "WHERE fundname LIKE "
    for i in range(len(FundNames)-1):
        FundNamesStr = FundNamesStr + "'"+FundNames[i]+"%' OR fundname LIKE "
    
    FundNamesStr = FundNamesStr +"'"+ FundNames[i+1]+"%'"
    #print(FundNamesStr)
    FundData = DBAction.LoadFund(myConnection,FundNamesStr)
    #FundData = DBAction.LoadFundOld(myConnection)
    #print(FundData)
    #print(FundData[0][0])
    #print(FundData[0][1])
    for i in range(len(FundData)):
        vals.append(FundData[i][1])
        cutvals.append(vals[i][(5478-WorkDaysAfter-WorkDaysBetween):(5478-WorkDaysAfter)]) #留最近一年的資料
    
    #print(cutvals[1])
    print("cutvalsssss:",cutvals)
    #print(vals)
    CalStart = time.time()
    #cov = np.cov(vals)
    cov = CovCorAction.cov_jit(cutvals)
    #print(cov)
    
    #cor = np.corrcoef(vals)
    cor = CovCorAction.corrcoef_jit(cutvals)
    #print("Cor",cor)
    CalStop = time.time()
    print("Cal",CalStop - CalStart)
    #Insert Data 
    dataArray = []
    for i in range(len(FundData)):
        dataArray.append(  (FundData[i][0],str(CovCorAction.TheDay),CovCorAction.timeinterval,1,cov[i].tolist())) #covcor 1表示是cov
        dataArray.append(   (FundData[i][0],str(CovCorAction.TheDay),CovCorAction.timeinterval,2,cor[i].tolist()))
     
    #DBAction.InsertData(myConnection,dataArray)
    #print(cov[0].tolist())
    #for i in range(len(FundData)): #單筆insert
     #   Insert(myConnection,FundData[i][0],"2016/10/19","1Y",1,cov[i].tolist())
      #  Insert(myConnection,FundData[i][0],"2016/10/19","1Y",2,cor[i].tolist())
    
    #WriteFile("CovCorData.txt",dataArray) #寫進txt檔
    """
    cur = myConnection.cursor()
    cur.execute("SELECT fund,date,timeinterval,covcor,value FROM covcortest2")
    print(cur.fetchall())"""
    
    AllTStop = time.time()
    print("All",AllTStop - AllTStart)    
         
    myConnection.commit()
    myConnection.close()
    
    print(cor)
    
    return cov,cor
    
if __name__ == "__main__":
    #if the user chooses some funds, date and timeinterval, then send some fund names to here
    FundNames = ["F0000000DG_InUSD","F0000000DH_InUSD","F0000000EM_InUSD","F0000000EN_InUSD","F0000000ER_InUSD","F0000000F5_InUSD","F0000000IR_InUSD","F0000000K1_InUSD","F0000000K2_InUSD","F0000000KM_InUSD"]
    TheDay = date(2016,10,19)
    timeinterval = '1Y'
    cov,cor = GetCorMatrix(FundNames,TheDay,timeinterval)
    #print(cov)
    #print(cor)
    
