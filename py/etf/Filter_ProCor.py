from __future__ import print_function
# -*- coding: utf-8 -*-
#!/usr/bin/env python3
from dateutil import rrule
import time
import sys
import json
import math
import numpy as np
from datetime import date,timedelta
from db_connection import DAO

def eprint(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs)

np.seterr(divide='ignore', invalid='ignore')

def ProCorFilter(JsonStr):
	data = json.loads(JsonStr)
	fundList = data['fundList']
	SelectDate = data['SelectDate']
	CorNum = data['corNum']
	profitNum = data['profitNum']
	aum_selected = data['aum_selected']

	#存結果的變數
	result_id = []

	#日期轉換
	timeStr = SelectDate.split('-')
	date_start_obj = date(2000, 1, 1)
	TheDay = date(int(timeStr[0]), int(timeStr[1]), int(timeStr[2]))
	workdays = get_working_days(date_start_obj, TheDay)

	#順列排序
	fundAry = fundList.split(',')
	fundAry = sorted(fundAry)

	matrix_start_time = time.time()
	corMatrix = GetCorMatrix(fundAry,workdays)
	matrix_end_time = time.time()


	#Matrix - 左上右下斜線給於極大值
	rows = corMatrix.shape[0]
	cols = corMatrix.shape[1]           
	for i in range(0, rows):
		for j in range(0, cols):
			if i==j:
				corMatrix[i][j]=999.0
	#Matrix - 取絕對值
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
		#Cor要求數量只有一個的時候greedy method，取一個最低
		resultSet.add(axis_x)
		resourceSet.discard(axis_x)
	elif int(CorNum)>=2:
		#Cor要求數量大於等於2時，先取出最低兩位
		resultSet.add(axis_x)
		resultSet.add(axis_y)
		resourceSet.discard(axis_x)
		resourceSet.discard(axis_y)
		#建立相加矩陣
		turnSum = np.zeros((1, x))
		for i in range(2,int(CorNum)):
			#已經取出來者之column直排相加
			for j in resultSet:
				turnSum += corMatrix[j][:]
			minimalPoint = np.argmin(turnSum)
			axis_yy = minimalPoint%(x)
			resultSet.add(axis_yy)
			resourceSet.discard(axis_yy)
			turnSum = np.zeros((1, x))

	#扣掉算出cor後剩下的部份，供下階段算profit使用
	resourceList = list(resourceSet)

	# cor 得到之結果加入result
	for i in resultSet:
		result_id.append(fundAry[i])

	############################
	## Profit  Calculation    ## 
	############################
	has_profit=0
	if int(profitNum) > 0:
		has_profit=1

		conn = DAO().connection()
		cur = conn.cursor(buffered=True)
		#計算日期
		timeStr = SelectDate.split('-')
		date_start_obj = date(2000, 1, 1)
		date_end_obj = date(int(timeStr[0]), int(timeStr[1]), int(timeStr[2]))
		workdays = get_working_days(date_start_obj, date_end_obj)
		returnrateAry = []
		#二維陣列 以returnrate大到小排列
		sql = "select returnrate,etf_id from etf_risk_profit_rank where timeinterval=20 and date="+str(workdays)+" and ("
		for i in resourceList:
			sql = sql + "(etf_id=\'"+str(fundAry[i])+"\')or"
		sql = sql[:-2] +") order by returnrate desc"
		cur.execute(sql)
		for result in cur.fetchall() :
			returnrateAry.append([float(result[0]),str(result[1])])

		# profit 得到之結果加入result
		for j in range(0,int(profitNum)):
			result_id.append(str(returnrateAry[j][1]))


	#重新按照字母排列一次，方便後續取名對應
	result_id = sorted(result_id)


	#回傳前端之方便split取陣列格式: result -> result_str
	result_str = "" 
	for k in result_id:
		result_str += str(k)+" "

	#取全名
	conn = DAO().connection()
	cur_NameList = conn.cursor(buffered=True)
	sql = "select etf_id,etfname "
	sql += "from just_raw_name_us "
	sql += "where "
	for i in result_id:
		sql += "(etf_id=\'"+str(i)+"\')or"
	sql = sql[:-2]+" order by  etf_id asc"
	cur_NameList.execute(sql)
	fullname_str = ""
	for i in cur_NameList.fetchall():
		fullname_str+=str(i[1])+"||"

	#若aum不為空，要加入aum，取aum全名
	fullname_aum_str = ""
	if (aum_selected!=""):
		aum_ary = aum_selected.split(" ")
		conn = DAO().connection()
		cur_NameList_aum = conn.cursor(buffered=True)
		sql = "select etf_id,etfname "
		sql += "from just_raw_name_us "
		sql += "where "
		for i in aum_ary:
			sql += "(etf_id=\'"+str(i)+"\')or"
		sql = sql[:-2]+" order by etf_id asc"
		cur_NameList_aum.execute(sql)
		fullname_aum_str = ""
		for i in cur_NameList_aum.fetchall():
			fullname_aum_str+=str(i[1])+"||"
		




	print(result_str)
	print(fullname_str)
	print(aum_selected)
	print(fullname_aum_str)
	print(corMatrix)
	print(" generating matrix using - "+ str(matrix_end_time-matrix_start_time))
	print(" matrix len = "+ str(x))
	print(" CorNum = "+ str(CorNum))
	print(" ProfitNum = "+ str(profitNum))
	if has_profit == 1:
		print("Profit_SortedAry = ",returnrateAry)
	print("day="+str(workdays))

def GetCorMatrix(fundAry,TheDay):
	thisDay = int(TheDay)
	timeInterval = 10

	#SQL Statment Generater
	sql = "select close,etf_id,date from etf_risk_profit_rank where timeinterval=10 and ("
	for i in fundAry:
		sql = sql + "(etf_id=\'"+str(i)+"\')or"
	sql = sql[:-2] +") and ("
	for j in range(0,timeInterval):
		sql = sql + "(date="+str(thisDay-j)+")or"
	sql = sql[:-2] +")  order by  etf_id asc,date asc"

	conn = DAO().connection()
	cur = conn.cursor(buffered=True)
	cur.execute(sql)
	Outer = []
	Insider = []
	temp_all_val = []
	
	counter = 0
	for result in cur.fetchall() :
		if counter<(len(fundAry)*timeInterval): #避免因為資料庫中的多冗值導致matrix不對稱error
			temp_all_val.append(result[0])
		counter+=1

	counter = 0
	for result in temp_all_val:
		Insider.append(result)
		counter += 1
		if counter == timeInterval:
			counter = 0
			Outer.append(Insider)
			Insider = []

	Outer = np.array(Outer)

	cor = cor_jit(Outer)
	return cor


#@jit(nogil = True,nopython = False)
def cor_jit(valueSet):
	return np.corrcoef(valueSet)

def get_working_days(date_start_obj, date_end_obj):
    weekdays = rrule.rrule(rrule.DAILY, byweekday=range(0, 5), dtstart=date_start_obj, until=date_end_obj)
    weekdays = list(weekdays)
    return len(weekdays)


if __name__ == "__main__":
	if sys.argv[1]=='ProCorFilter':
		ProCorFilter(sys.argv[2])
