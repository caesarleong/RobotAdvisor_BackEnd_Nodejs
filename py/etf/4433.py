#using etf_daily_net_worth
from dateutil import rrule
from datetime import date
import time
import psycopg2
import sys
import json
import numpy as np

hostname = 'localhost'
username = 'postgres'
password = 'test123'
database = 'mytest'
port = 5432

def calculate_4433(JsonStr):
	data = json.loads(JsonStr)
	selectDate = data['selectDate']
	rank_3m = int(data['rank_3m'])
	rank_6m = int(data['rank_6m'])
	rank_1y = int(data['rank_1y'])
	rank_2y = int(data['rank_2y'])
	rank_3y = int(data['rank_3y'])
	rank_5y = int(data['rank_5y'])

	#convert date to integer index.
	timeStr = selectDate.split('-')
	date_start_obj = date(2000, 1, 1)
	date_end_obj = date(int(timeStr[0]), int(timeStr[1]), int(timeStr[2]))
	workdays = get_working_days(date_start_obj, date_end_obj)

	#get source data
	SourceDataAry = GetData(workdays)
	##(3649, 4380, 168.52), (3649, 4320, 167.22), (3649, 4260, 160.62), (3649, 4140, 154.82), (3649, 3900, 153.4),(3649, 3660, 154.82), (3649, 3180, 153.4)

	#Construct return_rate array
	index = int(len(SourceDataAry)/7)
	dataAry = np.zeros(shape=(index,7))
	## [[theDay,3m,6m,1y,2y,3y,5y],...(3651),]
	## example dataAry: [ 39.05  37.11  34.87  34.26  33.57 34.66  37.57]

	counter_sub = 0
	counter_index = 0
	fund_id_list = []
	#counter_index是為了怕fund_id有跳號的狀況而設置的
	for j in SourceDataAry:
		dataAry[counter_index][counter_sub]=j[2]
		counter_sub += 1
		if counter_sub==7:
			fund_id_list.append(j[0])
			counter_sub=0
			counter_index += 1

	##example returnRate_3m: [0.008787, 1]...[0.003928, 3651]
	returnRate_3m=[]
	returnRate_6m=[]
	returnRate_1y=[]
	returnRate_2y=[]
	returnRate_3y=[]
	returnRate_5y=[]

	counter = 1
	for k in dataAry:
		#如果回推的那一天沒有基金資料，基本上我們就排除掉這隻
		#3m
		if k[1]==0:
			returnRate_3m.append([-999,counter])
		else:
			returnRate_3m.append([(k[0]-k[1])/k[1],counter])
		#6m
		if k[2]==0:
			returnRate_6m.append([-999,counter])
		else:
			returnRate_6m.append([(k[0]-k[2])/k[2],counter])
		#1y
		if k[3]==0:
			returnRate_1y.append([-999,counter])
		else:
			returnRate_1y.append([(k[0]-k[3])/k[3],counter])
		#2y
		if k[4]==0:
			returnRate_2y.append([-999,counter])
		else:
			returnRate_2y.append([(k[0]-k[4])/k[4],counter])
		#3y
		if k[5]==0:
			returnRate_3y.append([-999,counter])
		else:
			returnRate_3y.append([(k[0]-k[5])/k[5],counter])
		#5y
		if k[6]==0:
			returnRate_5y.append([-999,counter])
		else:
			returnRate_5y.append([(k[0]-k[6])/k[6],counter])
		counter+=1

	sorted_3m = sorted(returnRate_3m, reverse=True)
	sorted_6m = sorted(returnRate_6m, reverse=True)
	sorted_1y = sorted(returnRate_1y, reverse=True)
	sorted_2y = sorted(returnRate_2y, reverse=True)
	sorted_3y = sorted(returnRate_3y, reverse=True)
	sorted_5y = sorted(returnRate_5y, reverse=True)

	#產生符合要求排名的各個時間粒度之Set
	resultSet_3m = set()
	resultSet_6m = set()
	resultSet_1y = set()
	resultSet_2y = set()
	resultSet_3y = set()
	resultSet_5y = set()
	for i in range(0,rank_3m):
		resultSet_3m.add(sorted_3m[i][1])
	for i in range(0,rank_6m):
		resultSet_6m.add(sorted_6m[i][1])
	for i in range(0,rank_1y):
		resultSet_1y.add(sorted_1y[i][1])
	for i in range(0,rank_2y):
		resultSet_2y.add(sorted_2y[i][1])
	for i in range(0,rank_3y):
		resultSet_3y.add(sorted_3y[i][1])
	for i in range(0,rank_5y):
		resultSet_5y.add(sorted_5y[i][1])

	#取得最終交集
	u = set.intersection(resultSet_3m, resultSet_6m, resultSet_1y,resultSet_2y,resultSet_3y,resultSet_5y)

	#輸出string
	resultList = list(u)
	respondStr = ""
	for k in resultList:
		respondStr = respondStr+str(fund_id_list[k-1])+" "
		#id-1才會對應到index

	print(respondStr)


def GetData(workdays):
	myConnection = psycopg2.connect( host=hostname, user=username, password=password, database=database, port=port )
	cur  = myConnection.cursor()
	#資料庫裡面的時間長度不足，這裡是暫時性作法，把區間間距稍微調小
	#正確應該是 60 120 240 480 720 1200  然後timeinterval應該要取一年
	sql_stat = "select fund_id,date,returnrate from etf_risk_profit_rank "
	sql_stat += "where ((date="+str(workdays)+") or (date="+str(workdays)+"-60) or (date="+str(workdays)+"-120) or (date="+str(workdays)+"-240) or (date="+str(workdays)+"-360) "
	sql_stat += "or (date="+str(workdays)+"-480) or (date="+str(workdays)+"-600)) "
	sql_stat += "and timeinterval=65 order by fund_id asc ,date desc"
	cur.execute(sql_stat)
	return cur.fetchall()


def get_working_days(date_start_obj, date_end_obj):
    weekdays = rrule.rrule(rrule.DAILY, byweekday=range(0, 5), dtstart=date_start_obj, until=date_end_obj)
    weekdays = list(weekdays)
    return len(weekdays)



if __name__ == "__main__":
	if sys.argv[1]=='4433':
		calculate_4433(sys.argv[2])