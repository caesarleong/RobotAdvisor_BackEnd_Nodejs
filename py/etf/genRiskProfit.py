# -*- coding: utf-8 -*-
#!/usr/bin/env python3
from datetime import date
import random
import numpy as np
import time, sys, json
from db_connection import DAO

def get_working_days(start_date, end_date):
    from dateutil import rrule
    return len(list(rrule.rrule(rrule.DAILY, byweekday=range(0, 5), dtstart=start_date, until=end_date)))


def get_xy_fromsql(selected_date, selected_type):
	time_str = selected_date.split('-')
	start_date = date(2000, 1, 1)
	end_date = date(int(time_str[0]), int(time_str[1]), int(time_str[2]))
	select_day = get_working_days(start_date, end_date) - 1
	selected_type = selected_type

	conn = DAO().connection()

	##
	##  取得淨值資料 
	##

	cur_1m = conn.cursor(buffered=True)
	cur_3m = conn.cursor(buffered=True)
	cur_6m = conn.cursor(buffered=True)
	cur_1y = conn.cursor(buffered=True)
	cur_2y = conn.cursor(buffered=True)
	cur_3y = conn.cursor(buffered=True)
	cur_hasdata = conn.cursor(buffered=True)

	#check if 3 years ago have data
	have_3y_data=[]
	cur_hasdata.execute("select distinct etf_id from etf_risk_profit_rank where date=" + str(select_day-780) + " and close!=0")
	for result_obj in cur_hasdata.fetchall():
		have_3y_data.append(result_obj[0])

	if selected_type =="Daily Net Worth":
		cur_1m.execute("select distinct etf_id, sd, returnrate from etf_risk_profit_rank where date=" + str(select_day) + " and timeinterval=20 and returnrate!='NaN' and returnrate!='Infinity' and returnrate!=0 and sd!='Nan' and close!=0 order by etf_id asc" )
		cur_3m.execute("select distinct etf_id, sd, returnrate from etf_risk_profit_rank where date=" + str(select_day) + " and timeinterval=65 and returnrate!='NaN' and returnrate!='Infinity' and returnrate!=0 and sd!='Nan' and close!=0 order by etf_id asc" )
		cur_6m.execute("select distinct etf_id, sd, returnrate from etf_risk_profit_rank where date=" + str(select_day) + " and timeinterval=130 and returnrate!='NaN' and returnrate!='Infinity' and returnrate!=0 and sd!='Nan' and close!=0 order by etf_id asc" )
		cur_1y.execute("select distinct etf_id, sd, returnrate from etf_risk_profit_rank where date=" + str(select_day) + " and timeinterval=260 and returnrate!='NaN' and returnrate!='Infinity' and returnrate!=0 and sd!='Nan' and close!=0 order by etf_id asc" )
		cur_2y.execute("select distinct etf_id, sd, returnrate from etf_risk_profit_rank where date=" + str(select_day) + " and timeinterval=520 and returnrate!='NaN' and returnrate!='Infinity' and returnrate!=0 and sd!='Nan' and close!=0 order by etf_id asc" )
		cur_3y.execute("select distinct etf_id, sd, returnrate from etf_risk_profit_rank where date=" + str(select_day) + " and timeinterval=780 and returnrate!='NaN' and returnrate!='Infinity' and returnrate!=0 and sd!='Nan' and close!=0 order by etf_id asc" )


	if selected_type =="MA10":
		cur_1m.execute("select distinct etf_id, sd, returnrate from etf_sma_risk_profit_rank where date=" + str(select_day) + " and timeinterval=20 and sma_day=10 and returnrate!='NaN' and returnrate!='Infinity' and returnrate!='-1' and sd!='Nan' order by etf_id asc" )
		cur_3m.execute("select distinct etf_id, sd, returnrate from etf_sma_risk_profit_rank where date=" + str(select_day) + " and timeinterval=65 and sma_day=10 and returnrate!='NaN' and returnrate!='Infinity' and returnrate!='-1' and sd!='Nan' order by etf_id asc" )
		cur_6m.execute("select distinct etf_id, sd, returnrate from etf_sma_risk_profit_rank where date=" + str(select_day) + " and timeinterval=130 and sma_day=10 and returnrate!='NaN' and returnrate!='Infinity' and returnrate!='-1' and sd!='Nan' order by etf_id asc" )
		cur_1y.execute("select distinct etf_id, sd, returnrate from etf_sma_risk_profit_rank where date=" + str(select_day) + " and timeinterval=260 and sma_day=10 and returnrate!='NaN' and returnrate!='Infinity' and returnrate!='-1' and sd!='Nan' order by etf_id asc" )
		cur_2y.execute("select distinct etf_id, sd, returnrate from etf_sma_risk_profit_rank where date=" + str(select_day) + " and timeinterval=520 and sma_day=10 and returnrate!='NaN' and returnrate!='Infinity' and returnrate!='-1' and sd!='Nan' order by etf_id asc" )
		cur_3y.execute("select distinct etf_id, sd, returnrate from etf_sma_risk_profit_rank where date=" + str(select_day) + " and timeinterval=780 and sma_day=10 and returnrate!='NaN' and returnrate!='Infinity' and returnrate!='-1' and sd!='Nan' order by etf_id asc" )

	if selected_type =="MA20":
		cur_1m.execute("select distinct etf_id, sd, returnrate from etf_sma_risk_profit_rank where date=" + str(select_day) + " and timeinterval=20 and sma_day=20 and returnrate!='NaN' and returnrate!='Infinity' and returnrate!='-1' and sd!='Nan' order by etf_id asc" )
		cur_3m.execute("select distinct etf_id, sd, returnrate from etf_sma_risk_profit_rank where date=" + str(select_day) + " and timeinterval=65 and sma_day=20 and returnrate!='NaN' and returnrate!='Infinity' and returnrate!='-1' and sd!='Nan' order by etf_id asc" )
		cur_6m.execute("select distinct etf_id, sd, returnrate from etf_sma_risk_profit_rank where date=" + str(select_day) + " and timeinterval=130 and sma_day=20 and returnrate!='NaN' and returnrate!='Infinity' and returnrate!='-1' and sd!='Nan' order by etf_id asc" )
		cur_1y.execute("select distinct etf_id, sd, returnrate from etf_sma_risk_profit_rank where date=" + str(select_day) + " and timeinterval=260 and sma_day=20 and returnrate!='NaN' and returnrate!='Infinity' and returnrate!='-1' and sd!='Nan' order by etf_id asc" )
		cur_2y.execute("select distinct etf_id, sd, returnrate from etf_sma_risk_profit_rank where date=" + str(select_day) + " and timeinterval=520 and sma_day=20 and returnrate!='NaN' and returnrate!='Infinity' and returnrate!='-1' and sd!='Nan' order by etf_id asc" )
		cur_3y.execute("select distinct etf_id, sd, returnrate from etf_sma_risk_profit_rank where date=" + str(select_day) + " and timeinterval=780 and sma_day=20 and returnrate!='NaN' and returnrate!='Infinity' and returnrate!='-1' and sd!='Nan' order by etf_id asc" )

	output_json_1m = []
	for result_obj in cur_1m.fetchall():
		if(result_obj[0] in have_3y_data):
			output_json_1m.append({"id":result_obj[0], "x":result_obj[1], "y":result_obj[2]})

	output_json_3m = []
	for result_obj in cur_3m.fetchall():
		if(result_obj[0] in have_3y_data):
			output_json_3m.append({"id":result_obj[0], "x":result_obj[1], "y":result_obj[2]})

	output_json_6m = []
	for result_obj in cur_6m.fetchall():
		if(result_obj[0] in have_3y_data):
			output_json_6m.append({"id":result_obj[0], "x":result_obj[1], "y":result_obj[2]})

	output_json_1y = []
	for result_obj in cur_1y.fetchall():
		if(result_obj[0] in have_3y_data):
			output_json_1y.append({"id":result_obj[0], "x":result_obj[1], "y":result_obj[2]})
	
	output_json_2y = []
	for result_obj in cur_2y.fetchall():
		if(result_obj[0] in have_3y_data):
			output_json_2y.append({"id":result_obj[0], "x":result_obj[1], "y":result_obj[2]})
	
	output_json_3y = []
	for result_obj in cur_3y.fetchall():
		if(result_obj[0] in have_3y_data):
			output_json_3y.append({"id":result_obj[0], "x":result_obj[1], "y":result_obj[2]})
	

	print(json.dumps(output_json_1m))
	print(json.dumps(output_json_3m))
	print(json.dumps(output_json_6m))
	print(json.dumps(output_json_1y))
	print(json.dumps(output_json_2y))
	print(json.dumps(output_json_3y))

	##
	##  取得該日基金清單 
	##


	cur_NameList = conn.cursor(buffered=True)
	sql = "select a.etf_id,b.etfname "
	sql += "from etf_risk_profit_rank as a "
	sql += "left join just_raw_name_us as b "
	sql += "on a.etf_id= b.etf_id "
	sql += "where (a.date="+ str(select_day) +" and a.timeinterval=780) "
	sql += "order by a.etf_id asc"

	cur_NameList.execute(sql)

	output_NameList = []
	for result_obj in cur_NameList.fetchall():
		output_NameList.append({"name":result_obj[0],"full_name":result_obj[1]})
	print(json.dumps(output_NameList))

	conn.commit()
	conn.close()


if __name__ == "__main__":
    if sys.argv[1]=='genRiskProfit':
    	get_xy_fromsql(sys.argv[2], sys.argv[3])
