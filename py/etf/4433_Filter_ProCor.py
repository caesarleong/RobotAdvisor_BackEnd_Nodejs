# -*- coding: utf-8 -*-
#!/usr/bin/env python3
from dateutil import rrule
import time
import psycopg2
import sys
import json
import math
from CovCorDAO import CovCorDAO
import numpy as np
from datetime import date,timedelta
from CovCor import CovCor
from numba import jit, autojit,int32,cuda

np.seterr(divide='ignore', invalid='ignore')

hostname = 'localhost'
username = 'postgres'
password = 'test123'
database = 'mytest'
port = 5432


def ProCorFilter(JsonStr):
	data = json.loads(JsonStr)
	fundList = data['fundList']
	SelectDate = data['SelectDate']
	CorNum = data['corNum']
	profitNum = data['profitNum']

	#convert date to integer index.
	timeStr = SelectDate.split('-')
	date_start_obj = date(2000, 1, 1)
	TheDay = date(int(timeStr[0]), int(timeStr[1]), int(timeStr[2]))
	workdays = get_working_days(date_start_obj, TheDay)

	#Convert the fund_id to fund_name_list
	fundAry = fundList.split(',')
	fundidList = []
	for i in fundAry:
		fundidList.append(i)
	fundidStr = ""
	for i in fundAry:
		fundidStr = fundidStr+str(i)+" "
	print(fundidStr)
	matrix_start_time = time.time()
	corMatrix = GetCorMatrix(fundidList,workdays)	
	matrix_end_time = time.time()

	#Matrix - Generate 1 to 999
	rows = corMatrix.shape[0]
	cols = corMatrix.shape[1]                    
	for i in range(0, rows):
		for j in range(0, cols):
			if i==j:
				corMatrix[i][j]=999.0
	#Matrix - abs
	corMatrix = np.abs(corMatrix)

	############################
	###  Cor  Calculation    ### 
	############################
	calculation_start_time = time.time()

	x = len(fundAry) #Matrix size
	resultSet=set()
	resourceSet=set(np.arange(len(fundAry)))

	minimalPoint = np.argmin(corMatrix)
	axis_x = int(minimalPoint/x)
	axis_y = minimalPoint%(x)

	if int(CorNum)<2 and int(CorNum)>0:
		resultSet.add(axis_x)
		resourceSet.discard(axis_x)
	elif int(CorNum)>=2:
		#Selection more than two.
		resultSet.add(axis_x)
		resultSet.add(axis_y)
		resourceSet.discard(axis_x)
		resourceSet.discard(axis_y)
		#Summing resultSet to find next
		turnSum = np.zeros((1, x))
		#How many funds.
		for i in range(2,int(CorNum)):
			#Sum all result sets
			for j in resultSet:
				turnSum += corMatrix[j][:]
			minimalPoint = np.argmin(turnSum)
			axis_yy = minimalPoint%(x)
			resultSet.add(axis_yy)
			resourceSet.discard(axis_yy)
			turnSum = np.zeros((1, x))

	resourceList = list(resourceSet)

	############################
	## Profit  Calculation    ## 
	############################
	flag = 0
	if int(profitNum) > 0:
		myConnection = psycopg2.connect( host=hostname, user=username, password=password, database=database, port=port )
		cur = myConnection.cursor()
		#convert date to integer index.
		timeStr = SelectDate.split('-')
		date_start_obj = date(2000, 1, 1)
		date_end_obj = date(int(timeStr[0]), int(timeStr[1]), int(timeStr[2]))
		workdays = get_working_days(date_start_obj, date_end_obj)
		#get data from DB.
		returnrateAry = []
		sql = "select returnrate,fund_id from etf_risk_profit_rank where timeinterval=10 and date="+str(workdays)+" and ("
		for i in resourceList:
			sql = sql + "(fund_id="+str(fundAry[i])+")or"
		sql = sql[:-2] +")"
		cur.execute(sql)
		for result in cur.fetchall() :
			returnrateAry.append([float(result[0]),int(result[1])])
		
		for i in returnrateAry:
			for j in range(0,len(fundAry)-1):
				if i[1]==fundAry[j]:
					i[1]==j


		Ary_ReturnWithIndex = []
		
		for i in range(0,len(resourceList)-1):
			Ary_ReturnWithIndex.append([returnrateAry[i],resourceList[i]])
		
		flag = 1	
		SortedAry = sorted(Ary_ReturnWithIndex)
		for i in range(0,profitNum):
			resultSet.add(SortedAry[len(SortedAry)-1-i][1])
			resourceSet.discard(SortedAry[len(SortedAry)-1-i][1])

	### Calculation Done. ###
	calculation_end_time = time.time()

	#Error Handler.
	errflag = 0
	errNum = 0
	if len(resultSet) < CorNum+profitNum:
		errNum=len(resultSet)
		errflag=1
		resourceList2 = list(resourceSet)
		for i in range(0,CorNum+profitNum-len(resultSet)):
			resultSet.add(resourceList2[i])
			resourceSet.discard(resourceList2[i])

	#Output  resultString
	resultList = list(resultSet)
	resultStr = ""
	for k in resultList:
		resultStr = resultStr+str(k)+" "

	print(resultStr)

	#Output  FundNames
	#暫時使用昱銘的db，之後要改
	myConnection2 = psycopg2.connect( host='140.119.19.108', user='mlstd', password='iloveml', database='mlclass', port=5432 )
	cur = myConnection2.cursor()
	Result_fundName = ""
	sql = "select etfname from etf_name where "
	for k in resultList:
		sql+="(etf_id="+str(fundidList[k])+")or"
	sql = sql[:-2]
	cur.execute(sql)
	for result in cur.fetchall() :
		s = str(result[0])
		s = s.strip()
		Result_fundName += s+" "	

	print(Result_fundName)
	print(corMatrix)
	print(" generating matrix using - "+ str(matrix_end_time-matrix_start_time))
	print(" calculation using - "+ str(calculation_end_time-calculation_start_time))
	print(" matrix len = "+ str(x))
	print(" CorNum = "+ str(CorNum))
	print(" ProfitNum = "+ str(profitNum))
	print("resourceList = ",resourceList)
	if flag == 1:
		print("Profit_SortedAry = ",SortedAry)
	if errflag == 1:
		print("!!!!!!!ERROR: Number less than input.!!!! ",errNum)

def GetCorMatrix(fundidList,TheDay):
	thisDay = int(TheDay)
	timeInterval = 30

	#SQL Statment Generater
	sql = "select returnrate,fund_id,date from etf_risk_profit_rank where timeinterval=10 and ("
	for i in fundidList:
		sql = sql + "(fund_id="+str(i)+")or"
	sql = sql[:-2] +") and ("
	for j in range(0,timeInterval):
		sql = sql + "(date="+str(thisDay-j)+")or"
	sql = sql[:-2] +") order by fund_id asc,date asc"

	myConnection = psycopg2.connect( host=hostname, user=username, password=password, database=database, port=port )
	cur = myConnection.cursor()
	cur.execute(sql)
	Outer = []
	Insider = []
	counter = 0
	for result in cur.fetchall() :
		Insider.append(result[0])
		counter += 1
		if counter == timeInterval:
			counter = 0
			Outer.append(Insider)
			Insider = []
	cor = cor_jit(Outer)
	return cor


@jit(nogil = True,nopython = False)
def cor_jit(valueSet):
	return np.corrcoef(valueSet)

def get_working_days(date_start_obj, date_end_obj):
    weekdays = rrule.rrule(rrule.DAILY, byweekday=range(0, 5), dtstart=date_start_obj, until=date_end_obj)
    weekdays = list(weekdays)
    return len(weekdays)


if __name__ == "__main__":
	if sys.argv[1]=='ProCorFilter':
		ProCorFilter(sys.argv[2])
