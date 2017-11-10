# -*- coding: utf-8 -*-
#!/usr/bin/env python3
from datetime import date
import random
import numpy as np
import time, sys, json, psycopg2

hostname = 'localhost'
username = 'postgres'
password = 'test123'
database = 'mytest'
port = 5432

def get_working_days(start_date, end_date):
    from dateutil import rrule
    return len(list(rrule.rrule(rrule.DAILY, byweekday=range(0, 5), dtstart=start_date, until=end_date)))


def get_xy_fromsql(selected_date, selected_type):
	time_str = selected_date.split('-')
	start_date = date(2000, 1, 1)
	end_date = date(int(time_str[0]), int(time_str[1]), int(time_str[2]))
	select_day = get_working_days(start_date, end_date) - 1
	selected_type = selected_type

	conn = psycopg2.connect(host=hostname, user=username, password=password, database=database, port=port)
	cur_1m = conn.cursor()
	cur_3m = conn.cursor()
	cur_6m = conn.cursor()
	cur_1y = conn.cursor()
	cur_2y = conn.cursor()
	cur_3y = conn.cursor()

	if selected_type =="Daily Net Worth":
		cur_1m.execute("select distinct fund_id, sd, returnrate from etf_risk_profit_rank where date=" + str(select_day-20) + " and timeinterval=20 and returnrate!='NaN' and returnrate!='Infinity' and returnrate!='-1' and sd!='Nan' order by fund_id asc" )
		cur_3m.execute("select distinct fund_id, sd, returnrate from etf_risk_profit_rank where date=" + str(select_day-60) + " and timeinterval=20 and returnrate!='NaN' and returnrate!='Infinity' and returnrate!='-1' and sd!='Nan' order by fund_id asc" )
		cur_6m.execute("select distinct fund_id, sd, returnrate from etf_risk_profit_rank where date=" + str(select_day-120) + " and timeinterval=20 and returnrate!='NaN' and returnrate!='Infinity' and returnrate!='-1' and sd!='Nan' order by fund_id asc" )
		cur_1y.execute("select distinct fund_id, sd, returnrate from etf_risk_profit_rank where date=" + str(select_day-240) + " and timeinterval=20 and returnrate!='NaN' and returnrate!='Infinity' and returnrate!='-1' and sd!='Nan' order by fund_id asc" )
		cur_2y.execute("select distinct fund_id, sd, returnrate from etf_risk_profit_rank where date=" + str(select_day-480) + " and timeinterval=20 and returnrate!='NaN' and returnrate!='Infinity' and returnrate!='-1' and sd!='Nan' order by fund_id asc" )
		cur_3y.execute("select distinct fund_id, sd, returnrate from etf_risk_profit_rank where date=" + str(select_day-720) + " and timeinterval=20 and returnrate!='NaN' and returnrate!='Infinity' and returnrate!='-1' and sd!='Nan' order by fund_id asc" )


	if selected_type =="MA10":
		cur_1m.execute("select distinct fund_id, sd, returnrate from etf_sma_risk_profit_rank where date=" + str(select_day-20) + " and timeinterval=20 and sma_day=10 and returnrate!='NaN' and returnrate!='Infinity' and returnrate!='-1' and sd!='Nan' order by fund_id asc" )
		cur_3m.execute("select distinct fund_id, sd, returnrate from etf_sma_risk_profit_rank where date=" + str(select_day-60) + " and timeinterval=20 and sma_day=10 and returnrate!='NaN' and returnrate!='Infinity' and returnrate!='-1' and sd!='Nan' order by fund_id asc" )
		cur_6m.execute("select distinct fund_id, sd, returnrate from etf_sma_risk_profit_rank where date=" + str(select_day-120) + " and timeinterval=20 and sma_day=10 and returnrate!='NaN' and returnrate!='Infinity' and returnrate!='-1' and sd!='Nan' order by fund_id asc" )
		cur_1y.execute("select distinct fund_id, sd, returnrate from etf_sma_risk_profit_rank where date=" + str(select_day-240) + " and timeinterval=20 and sma_day=10 and returnrate!='NaN' and returnrate!='Infinity' and returnrate!='-1' and sd!='Nan' order by fund_id asc" )
		cur_2y.execute("select distinct fund_id, sd, returnrate from etf_sma_risk_profit_rank where date=" + str(select_day-480) + " and timeinterval=20 and sma_day=10 and returnrate!='NaN' and returnrate!='Infinity' and returnrate!='-1' and sd!='Nan' order by fund_id asc" )
		cur_3y.execute("select distinct fund_id, sd, returnrate from etf_sma_risk_profit_rank where date=" + str(select_day-720) + " and timeinterval=20 and sma_day=10 and returnrate!='NaN' and returnrate!='Infinity' and returnrate!='-1' and sd!='Nan' order by fund_id asc" )

	if selected_type =="MA20":
		cur_1m.execute("select distinct fund_id, sd, returnrate from etf_sma_risk_profit_rank where date=" + str(select_day-20) + " and timeinterval=20 and sma_day=20 and returnrate!='NaN' and returnrate!='Infinity' and returnrate!='-1' and sd!='Nan' order by fund_id asc" )
		cur_3m.execute("select distinct fund_id, sd, returnrate from etf_sma_risk_profit_rank where date=" + str(select_day-60) + " and timeinterval=20 and sma_day=20 and returnrate!='NaN' and returnrate!='Infinity' and returnrate!='-1' and sd!='Nan' order by fund_id asc" )
		cur_6m.execute("select distinct fund_id, sd, returnrate from etf_sma_risk_profit_rank where date=" + str(select_day-120) + " and timeinterval=20 and sma_day=20 and returnrate!='NaN' and returnrate!='Infinity' and returnrate!='-1' and sd!='Nan' order by fund_id asc" )
		cur_1y.execute("select distinct fund_id, sd, returnrate from etf_sma_risk_profit_rank where date=" + str(select_day-240) + " and timeinterval=20 and sma_day=20 and returnrate!='NaN' and returnrate!='Infinity' and returnrate!='-1' and sd!='Nan' order by fund_id asc" )
		cur_2y.execute("select distinct fund_id, sd, returnrate from etf_sma_risk_profit_rank where date=" + str(select_day-480) + " and timeinterval=20 and sma_day=20 and returnrate!='NaN' and returnrate!='Infinity' and returnrate!='-1' and sd!='Nan' order by fund_id asc" )
		cur_3y.execute("select distinct fund_id, sd, returnrate from etf_sma_risk_profit_rank where date=" + str(select_day-720) + " and timeinterval=20 and sma_day=20 and returnrate!='NaN' and returnrate!='Infinity' and returnrate!='-1' and sd!='Nan' order by fund_id asc" )

	output_json_1m = []
	for result_obj in cur_1m.fetchall():
		output_json_1m.append({"id":result_obj[0], "x":result_obj[1], "y":result_obj[2]})

	output_json_3m = []
	for result_obj in cur_3m.fetchall():
		output_json_3m.append({"id":result_obj[0], "x":result_obj[1], "y":result_obj[2]})

	output_json_6m = []
	for result_obj in cur_6m.fetchall():
		output_json_6m.append({"id":result_obj[0], "x":result_obj[1], "y":result_obj[2]})

	output_json_1y = []
	for result_obj in cur_1y.fetchall():
		output_json_1y.append({"id":result_obj[0], "x":result_obj[1], "y":result_obj[2]})
	
	output_json_2y = []
	for result_obj in cur_2y.fetchall():
		output_json_2y.append({"id":result_obj[0], "x":result_obj[1], "y":result_obj[2]})
	
	output_json_3y = []
	for result_obj in cur_3y.fetchall():
		output_json_3y.append({"id":result_obj[0], "x":result_obj[1], "y":result_obj[2]})
	

	print(json.dumps(output_json_1m))
	print(json.dumps(output_json_3m))
	print(json.dumps(output_json_6m))
	print(json.dumps(output_json_1y))
	print(json.dumps(output_json_2y))
	print(json.dumps(output_json_3y))

	conn.commit()
	conn.close()

	outside,name_obj = randomize_stock_data(select_day,selected_type)
	print(json.dumps(outside))
	print(json.dumps(name_obj))

	
def randomize_stock_data(select_day,selected_type):
	conn = psycopg2.connect(host=hostname, user=username, password=password, database=database, port=port)
	cur = conn.cursor()
	num = random.randint(3,8)
	#fund_id = np.random.randint(1,800, size=num)
	#fund_id = [46,470,746]
	fund_id = [46,167,746,470,115]

	if selected_type=="Daily Net Worth":
		sql = "select fund_id, sd, returnrate from etf_risk_profit_rank where timeinterval=65 and ("
		for counter in range(0,30):
			sql += "(date="+str(select_day-counter)+")or"
		sql = sql[:-2] +") and ("
		for id in fund_id:
			sql += "(fund_id="+str(id)+")or"
		sql = sql[:-2] +") order by fund_id asc,date asc"

	if selected_type =="MA10":
		sql = "select fund_id, sd, returnrate from etf_sma_risk_profit_rank where sma_day=10 and timeinterval=65 and ("
		for counter in range(0,30):
			sql += "(date="+str(select_day-counter)+")or"
		sql = sql[:-2] +") and ("
		for id in fund_id:
			sql += "(fund_id="+str(id)+")or"
		sql = sql[:-2] +") order by fund_id asc,date asc"

	if selected_type =="MA20":
		sql = "select fund_id, sd, returnrate from etf_sma_risk_profit_rank where sma_day=20 and timeinterval=65 and ("
		for counter in range(0,30):
			sql += "(date="+str(select_day-counter)+")or"
		sql = sql[:-2] +") and ("
		for id in fund_id:
			sql += "(fund_id="+str(id)+")or"
		sql = sql[:-2] +") order by fund_id asc,date asc"

	cur.execute(sql)

	#structure:  [  [first fund's 30 day {x,y}] [second fund's] [...] .. till fund numbers ]
	outside = []
	inside = []
	counter = 0
	for result in cur.fetchall() :
		inside.append({"x":result[1], "y":result[2]})
		counter += 1
		if counter == 30:
			counter = 0
			outside.append(inside)
			inside = []

	

	#find name
	sql_find_name = "select etf_id,etfname from etf_name where ("
	for id in fund_id:
		sql_find_name += "(etf_id="+str(id)+")or"
	sql_find_name = sql_find_name[:-2] +") order by etf_id asc"
	
	cur.execute(sql_find_name)
	name_obj = []
	for result in cur.fetchall() :
		name_obj.append({"id":result[0],"name":str(result[1]).strip()})

	return outside,name_obj

if __name__ == "__main__":
    if sys.argv[1]=='DC_genRiskProfit':
    	get_xy_fromsql(sys.argv[2], sys.argv[3])
