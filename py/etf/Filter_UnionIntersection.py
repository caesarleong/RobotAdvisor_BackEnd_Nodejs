# -*- coding: utf-8 -*-
#!/usr/bin/env python3

#0827  MA的部份還沒改！


from dateutil import rrule
from datetime import date
import time
import sys
import json
import math
from db_connection import DAO

hostname = 'localhost'
username = 'postgres'
password = 'test123'
database = 'mytest'
port = 5432

def UnionIntersection_lrr(JsonStr):
	conn = DAO().connection()

	data = json.loads(JsonStr)
	SelectDate = data['SelectDate']
	blocks_1m = data['blocks_1m']
	blocks_3m = data['blocks_3m']
	blocks_6m = data['blocks_6m']
	blocks_1y = data['blocks_1y']
	blocks_2y = data['blocks_2y']
	blocks_3y = data['blocks_3y']
	strategy_1m = data['strategy_1m']
	strategy_3m = data['strategy_3m']
	strategy_6m = data['strategy_6m']
	strategy_1y = data['strategy_1y']
	strategy_2y = data['strategy_2y']
	strategy_3y = data['strategy_3y']
	selected_type = data['selected_type']
	stock_list = data['aum_selected']

	#convert date to integer index.
	timeStr = SelectDate.split('-')
	date_start_obj = date(2000, 1, 1)
	date_end_obj = date(int(timeStr[0]), int(timeStr[1]), int(timeStr[2]))
	workdays = get_working_days(date_start_obj, date_end_obj)

	set_1m = set()
	set_3m = set()
	set_6m = set()
	set_1y = set()
	set_2y = set()
	set_3y = set()

	###### Daily Net Worth ###### 
	if selected_type=="Daily Net Worth":
		#1m
		if blocks_1m:
			sql_1m = "select etf_id from etf_risk_profit_rank "
			sql_1m += "where date="+str(workdays)+" and timeinterval='20' "
			sql_1m += "and ("
			for i in blocks_1m:
				sql_1m = sql_1m+" (rank_sd="+str(i['x'])+" and rank_rate="+str(i['y'])+") or"
			sql_1m = sql_1m[:-2] +") order by etf_id asc"
			cur  = conn.cursor(buffered=True)
			cur.execute(sql_1m)
			for j in cur.fetchall() :
				set_1m.add(j[0])

		#3m
		if blocks_3m:
			sql_3m = "select etf_id from etf_risk_profit_rank "
			sql_3m += "where date="+str(workdays)+" and timeinterval='65' "
			sql_3m += "and ("
			for i in blocks_3m:
				sql_3m = sql_3m+" (rank_sd="+str(i['x'])+" and rank_rate="+str(i['y'])+") or"
			sql_3m = sql_3m[:-2] +") order by etf_id asc"
			cur  = conn.cursor(buffered=True)
			cur.execute(sql_3m)
			for j in cur.fetchall() :
				set_3m.add(j[0])

		#6m
		if blocks_6m:
			sql_6m = "select etf_id from etf_risk_profit_rank "
			sql_6m += "where date="+str(workdays)+" and timeinterval='130' "
			sql_6m += "and ("
			for i in blocks_6m:
				sql_6m = sql_6m+" (rank_sd="+str(i['x'])+" and rank_rate="+str(i['y'])+") or"
			sql_6m = sql_6m[:-2] +") order by etf_id asc"
			cur  = conn.cursor(buffered=True)
			cur.execute(sql_6m)
			for j in cur.fetchall() :
				set_6m.add(j[0])

		#1y
		if blocks_1y:
			sql_1y = "select etf_id from etf_risk_profit_rank "
			sql_1y += "where date="+str(workdays)+" and timeinterval='260' "
			sql_1y += "and ("
			for i in blocks_1y:
				sql_1y = sql_1y+" (rank_sd="+str(i['x'])+" and rank_rate="+str(i['y'])+") or"
			sql_1y = sql_1y[:-2] +") order by etf_id asc"
			cur  = conn.cursor(buffered=True)
			cur.execute(sql_1y)
			for j in cur.fetchall() :
				set_1y.add(j[0])

		#2y
		if blocks_2y:
			sql_2y = "select etf_id from etf_risk_profit_rank "
			sql_2y += "where date="+str(workdays)+" and timeinterval='520' "
			sql_2y += "and ("
			for i in blocks_2y:
				sql_2y = sql_2y+" (rank_sd="+str(i['x'])+" and rank_rate="+str(i['y'])+") or"
			sql_2y = sql_2y[:-2] +") order by etf_id asc"
			cur  = conn.cursor(buffered=True)
			cur.execute(sql_2y)
			for j in cur.fetchall() :
				set_2y.add(j[0])

		#3y
		if blocks_3y:
			sql_3y = "select etf_id from etf_risk_profit_rank "
			sql_3y += "where date="+str(workdays)+" and timeinterval='780' "
			sql_3y += "and ("

			for i in blocks_3y:
				sql_3y = sql_3y+" (rank_sd="+str(i['x'])+" and rank_rate="+str(i['y'])+") or"
			sql_3y = sql_3y[:-2] +") order by etf_id asc"
			cur  = conn.cursor(buffered=True)
			cur.execute(sql_3y)
			for j in cur.fetchall() :
				set_3y.add(j[0])
	

	###### MA10 ###### 
	if selected_type =="MA10":
		#1m
		if blocks_1m:
			sql_1m = "select fund_id from etf_sma_risk_profit_rank "
			sql_1m += "where date="+str(workdays)+" and sma_day=10 and timeinterval='20' "
			sql_1m += "and returnrate!='NaN' and returnrate!='Infinity' and returnrate!=0 and ("
			for i in blocks_1m:
				sql_1m = sql_1m+" (rank_sd="+str(i['x'])+" and rank_rate="+str(i['y'])+") or"
			sql_1m = sql_1m[:-2] +") order by fund_id asc"
			cur  = myConnection.cursor()
			cur.execute(sql_1m)
			for j in cur.fetchall() :
				set_1m.add(j[0])

		#3m
		if blocks_3m:
			sql_3m = "select fund_id from etf_sma_risk_profit_rank "
			sql_3m += "where date="+str(workdays)+" and sma_day=10 and timeinterval='65' "
			sql_3m += "and returnrate!='NaN' and returnrate!='Infinity' and returnrate!=0 and ("
			for i in blocks_3m:
				sql_3m = sql_3m+" (rank_sd="+str(i['x'])+" and rank_rate="+str(i['y'])+") or"
			sql_3m = sql_3m[:-2] +") order by fund_id asc"
			cur  = myConnection.cursor()
			cur.execute(sql_3m)
			for j in cur.fetchall() :
				set_3m.add(j[0])

		#6m
		if blocks_6m:
			sql_6m = "select fund_id from etf_sma_risk_profit_rank "
			sql_6m += "where date="+str(workdays)+" and sma_day=10 and timeinterval='130' "
			sql_6m += "and returnrate!='NaN' and returnrate!='Infinity' and returnrate!=0 and ("
			for i in blocks_6m:
				sql_6m = sql_6m+" (rank_sd="+str(i['x'])+" and rank_rate="+str(i['y'])+") or"
			sql_6m = sql_6m[:-2] +") order by fund_id asc"
			cur  = myConnection.cursor()
			cur.execute(sql_6m)
			for j in cur.fetchall() :
				set_6m.add(j[0])

		#1y
		if blocks_1y:
			sql_1y = "select fund_id from etf_sma_risk_profit_rank "
			sql_1y += "where date="+str(workdays)+" and sma_day=10 and timeinterval='260' "
			sql_1y += "and returnrate!='NaN' and returnrate!='Infinity' and returnrate!=0 and ("
			for i in blocks_1y:
				sql_1y = sql_1y+" (rank_sd="+str(i['x'])+" and rank_rate="+str(i['y'])+") or"
			sql_1y = sql_1y[:-2] +") order by fund_id asc"
			cur  = myConnection.cursor()
			cur.execute(sql_1y)
			for j in cur.fetchall() :
				set_1y.add(j[0])

		#2y
		if blocks_2y:
			sql_2y = "select fund_id from etf_sma_risk_profit_rank "
			sql_2y += "where date="+str(workdays)+" and sma_day=10 and timeinterval='520' "
			sql_2y += "and returnrate!='NaN' and returnrate!='Infinity' and returnrate!=0 and ("
			for i in blocks_2y:
				sql_2y = sql_2y+" (rank_sd="+str(i['x'])+" and rank_rate="+str(i['y'])+") or"
			sql_2y = sql_2y[:-2] +") order by fund_id asc"
			cur  = myConnection.cursor()
			cur.execute(sql_2y)
			for j in cur.fetchall() :
				set_2y.add(j[0])

		#3y
		if blocks_3y:
			sql_3y = "select fund_id from etf_sma_risk_profit_rank "
			sql_3y += "where date="+str(workdays)+" and sma_day=10 and timeinterval='780' "
			sql_3y += "and returnrate!='NaN' and returnrate!='Infinity' and returnrate!=0 and ("

			for i in blocks_3y:
				sql_3y = sql_3y+" (rank_sd="+str(i['x'])+" and rank_rate="+str(i['y'])+") or"
			sql_3y = sql_3y[:-2] +") order by fund_id asc"
			cur  = myConnection.cursor()
			cur.execute(sql_3y)
			for j in cur.fetchall() :
				set_3y.add(j[0])

	###### MA20 ###### 
	if selected_type =="MA20":
		#1m
		if blocks_1m:
			sql_1m = "select fund_id from etf_sma_risk_profit_rank "
			sql_1m += "where date="+str(workdays)+" and sma_day=20 and timeinterval='20' "
			sql_1m += "and returnrate!='NaN' and returnrate!='Infinity' and returnrate!=0 and ("
			for i in blocks_1m:
				sql_1m = sql_1m+" (rank_sd="+str(i['x'])+" and rank_rate="+str(i['y'])+") or"
			sql_1m = sql_1m[:-2] +") order by fund_id asc"
			cur  = myConnection.cursor()
			cur.execute(sql_1m)
			for j in cur.fetchall() :
				set_1m.add(j[0])

		#3m
		if blocks_3m:
			sql_3m = "select fund_id from etf_sma_risk_profit_rank "
			sql_3m += "where date="+str(workdays)+" and sma_day=20 and timeinterval='65' "
			sql_3m += "and returnrate!='NaN' and returnrate!='Infinity' and returnrate!=0 and ("
			for i in blocks_3m:
				sql_3m = sql_3m+" (rank_sd="+str(i['x'])+" and rank_rate="+str(i['y'])+") or"
			sql_3m = sql_3m[:-2] +") order by fund_id asc"
			cur  = myConnection.cursor()
			cur.execute(sql_3m)
			for j in cur.fetchall() :
				set_3m.add(j[0])

		#6m
		if blocks_6m:
			sql_6m = "select fund_id from etf_sma_risk_profit_rank "
			sql_6m += "where date="+str(workdays)+" and sma_day=20 and timeinterval='130' "
			sql_6m += "and returnrate!='NaN' and returnrate!='Infinity' and returnrate!=0 and ("
			for i in blocks_6m:
				sql_6m = sql_6m+" (rank_sd="+str(i['x'])+" and rank_rate="+str(i['y'])+") or"
			sql_6m = sql_6m[:-2] +") order by fund_id asc"
			cur  = myConnection.cursor()
			cur.execute(sql_6m)
			for j in cur.fetchall() :
				set_6m.add(j[0])

		#1y
		if blocks_1y:
			sql_1y = "select fund_id from etf_sma_risk_profit_rank "
			sql_1y += "where date="+str(workdays)+" and sma_day=20 and timeinterval='260' "
			sql_1y += "and returnrate!='NaN' and returnrate!='Infinity' and returnrate!=0 and ("
			for i in blocks_1y:
				sql_1y = sql_1y+" (rank_sd="+str(i['x'])+" and rank_rate="+str(i['y'])+") or"
			sql_1y = sql_1y[:-2] +") order by fund_id asc"
			cur  = myConnection.cursor()
			cur.execute(sql_1y)
			for j in cur.fetchall() :
				set_1y.add(j[0])

		#2y
		if blocks_2y:
			sql_2y = "select fund_id from etf_sma_risk_profit_rank "
			sql_2y += "where date="+str(workdays)+" and sma_day=20 and timeinterval='520' "
			sql_2y += "and returnrate!='NaN' and returnrate!='Infinity' and returnrate!=0 and ("
			for i in blocks_2y:
				sql_2y = sql_2y+" (rank_sd="+str(i['x'])+" and rank_rate="+str(i['y'])+") or"
			sql_2y = sql_2y[:-2] +") order by fund_id asc"
			cur  = myConnection.cursor()
			cur.execute(sql_2y)
			for j in cur.fetchall() :
				set_2y.add(j[0])

		#3y
		if blocks_3y:
			sql_3y = "select fund_id from etf_sma_risk_profit_rank "
			sql_3y += "where date="+str(workdays)+" and sma_day=20 and timeinterval='780' "
			sql_3y += "and returnrate!='NaN' and returnrate!='Infinity' and returnrate!=0 and ("

			for i in blocks_3y:
				sql_3y = sql_3y+" (rank_sd="+str(i['x'])+" and rank_rate="+str(i['y'])+") or"
			sql_3y = sql_3y[:-2] +") order by fund_id asc"
			cur  = myConnection.cursor()
			cur.execute(sql_3y)
			for j in cur.fetchall() :
				set_3y.add(j[0])


	result = set()
	set_array = [set_1m,set_3m,set_6m,set_1y,set_2y,set_3y]
	strategy_array = [strategy_1m,strategy_3m,strategy_6m,strategy_1y,strategy_2y,strategy_3y]


	#判斷有沒有聯集交集的合法區塊
	has_Union = False
	hsa_Intersection = False
	for i in range(0,6):
		if (len(set_array[i])>1)and(strategy_array[i]=="Union"):
			has_Union = True
		if (len(set_array[i])>1)and(strategy_array[i]=="Intersection"):
			hsa_Intersection = True

	##都是選交集
	if(has_Union==False):
		#取出任意一個合法的intersection時間區段assign給result設定為初始值，預設最後一個取的
		for i in range(0,6):
			if (len(set_array[i])>1)and(strategy_array[i]=="Intersection"):
				result = set_array[i]
		#和其他合法的intersection時間區段取交集
		for i in range(0,6):
			if (len(set_array[i])>1)and(strategy_array[i]=="Intersection"):
				result = result & set_array[i]

	##有的交集，有的聯集
	if(has_Union==True)and(hsa_Intersection==True):
		#先取出只有聯集的區塊
		for i in range(0,6):
			if (len(set_array[i])>1)and(strategy_array[i]=="Union"):
				result = result | set_array[i]
		#再和交集的區塊逐一交集
		for i in range(0,6):
			if (len(set_array[i])>1)and(strategy_array[i]=="Intersection"):
				result = result & set_array[i]
	#都是聯集
	if(hsa_Intersection==False):
		for i in range(0,6):
			if (len(set_array[i])>1)and(strategy_array[i]=="Union"):
				result = result | set_array[i]

	#已經在user的uma list的就不要重複選出來了，排除掉
	stock_list = stock_list.strip().split(" ")
	for i in stock_list:
		result.discard(i)

	#0918 三年前沒資料的基金也要排除掉
	have_3y_data=set()
	cur_hasdata = conn.cursor(buffered=True)
	cur_hasdata.execute("select distinct etf_id from etf_risk_profit_rank where date=" + str(workdays-780) + " and close!=0")
	for result_obj in cur_hasdata.fetchall():
		have_3y_data.add(result_obj[0])
	result = result & have_3y_data

	res = ""
	for k in result:
		res = res+str(k)+" "
	print(res)
	
	conn.commit()
	conn.close()



def get_working_days(date_start_obj, date_end_obj):
    weekdays = rrule.rrule(rrule.DAILY, byweekday=range(0, 5), dtstart=date_start_obj, until=date_end_obj)
    weekdays = list(weekdays)
    weekdays = [day.strftime('%Y/%m/%d') for day in weekdays]
    return len(weekdays)

if __name__ == "__main__":
    if sys.argv[1]=='Union&Intersection':
    	UnionIntersection_lrr(sys.argv[2])
