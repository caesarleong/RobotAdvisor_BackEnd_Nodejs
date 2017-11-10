#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-
"""
Created on Wed Aug 30 20:29:31 2017

@author: benwu
"""
from db_connection import DAO
import numpy as np
import matplotlib.pyplot as plt
import cvxopt as opt
from cvxopt import blas, solvers, printing
from collections import namedtuple
import sys, json
from datetime import date
import math
from decimal import Decimal 


## cvxopt optimization portfolio
def optimal_portfolio(returns):
    np.set_printoptions(threshold=np.nan, linewidth=1200)
    printing.options['width'] = -1
    solvers.options['show_progress'] = False

    n = len(returns)
    returns = np.asmatrix(returns)
    
    N = 100
    mus = [10**(5.0 * t/N - 1.0) for t in range(N)]
    
    # Convert to cvxopt matrices
    S = opt.matrix(np.cov(returns))
    pbar = opt.matrix(np.mean(returns, axis=1))
    
    # Create constraint matrices
    G = -opt.matrix(np.eye(n))   # negative n x n identity matrix
    h = opt.matrix(0.0, (n ,1))
    A = opt.matrix(1.0, (1, n))
    b = opt.matrix(1.0)
    
    # Calculate efficient frontier weights using quadratic programming
    portfolios = [solvers.qp(mu*S, -pbar, G, h, A, b)['x']  for mu in mus]
    ## CALCULATE RISKS AND RETURNS FOR FRONTIER
    returns = [blas.dot(pbar, x) for x in portfolios]
    risks = [np.sqrt(blas.dot(x, S*x)) for x in portfolios]
    ## CALCULATE THE 2ND DEGREE POLYNOMIAL OF THE FRONTIER CURVE
    m1 = np.polyfit(returns, risks, 2)
    x1 = np.sqrt(abs(m1[2] / m1[0]))
    # CALCULATE THE OPTIMAL PORTFOLIO
    wt = solvers.qp(opt.matrix(x1 * S), -pbar, G, h, A, b)['x']
    return np.asarray(wt), np.asarray(returns), np.asarray(risks)
def random_portfolio(returns):
    ''' 
    Returns the mean and standard deviation of returns for a random portfolio
    '''

    p = np.asmatrix(np.mean(returns, axis=1))
    w = np.asmatrix(rand_weights(returns.shape[0]))
    C = np.asmatrix(np.cov(returns))
    
    mu = w * p.T
    sigma = np.sqrt(w * C * w.T)
    
    # This recursion reduces outliers to keep plots pretty
    #if sigma > 2:
    #    return random_portfolio(returns)
    return mu, sigma

def rand_weights(n):
    ''' Produces n random weights that sum to 1 '''
    k = np.random.rand(n)
    return k / sum(k)

def main(json_data):
    #ignore poor polyfit stderr message
    #stdout = sys.stdout
    #stderr = sys.stderr
    #sys.stdout = open('/dev/null', 'w')
    #sys.stderr  = open('/dev/null', 'w')
    
    data = json.loads(json_data)
    fund_result_id, select_date = data['FundResultID'], data['SelectDate']
    
    #convert date to integer index.
    timeStr = select_date.split('-')
    date_start_obj = date(2000, 1, 1)
    TheDay = date(int(timeStr[0]), int(timeStr[1]), int(timeStr[2]))
    select_day = get_working_days(date_start_obj, TheDay)


    conn = DAO().connection()
    cur = conn.cursor(buffered=True)
        
    sql = "select close from etf_risk_profit_rank where timeinterval=20 and ("
    for i in range(0, len(fund_result_id)):
        sql = sql + "(etf_id=\'" + str(fund_result_id[i]) + "\')or"
    sql = sql[:-2] + ") and ("
    for j in range(0, 130):
        sql = sql + "(date=" + str(select_day - j) + ")or"
    sql = sql[:-2] + ") order by etf_id asc,date asc"
        
    cur.execute(sql)
    close_arr = []
    for each in cur.fetchall():
        close_arr.append(each[0])

    return_vec = np.array(close_arr).reshape((-1, 130))

    weights, returns, risks = optimal_portfolio(return_vec)

    ratios = returns / risks

    #Generate Random Portfolio
    n_portfolios = 1000
    means, stds = np.column_stack([
        random_portfolio(return_vec) 
        for _ in range(n_portfolios)
    ])
    cstack = np.column_stack((stds,means))
    rand_ary_x = []
    rand_ary_y = []
    
    for i in cstack:
        if((i[0]<=risks[0]) and (i[1]>=returns[len(returns)-1])):
            rand_ary_x.append(i[0])
            rand_ary_y.append(i[1])


    fig, ax1 = plt.subplots()
    ax1.plot(risks, returns, '-b')
    ax1.plot(rand_ary_x,rand_ary_y,'o',ms=3)
    ax1.set_xlabel('standard deviation')
    ax1.set_ylabel('expected return', color='b', rotation=90, labelpad=0)
    ax1.tick_params('y', colors='b')
    ax2 = ax1.twinx()
    ax2.plot(risks, ratios, '--r')
    ax2.set_ylabel('sharp ratio', color='r', rotation=90, labelpad=0)
    ax2.tick_params('y', colors='r')


    ## save&base64
    from io import BytesIO
    fig_file = BytesIO()
    plt.savefig(fig_file, format='png')
    fig_file.seek(0)

    import base64
    fig_png = base64.b64encode(fig_file.getvalue())

    ## 取得基金id
    fund_result_id_str = ""
    sorted_fund_result_id = sorted(fund_result_id)
    for i in sorted_fund_result_id:
        fund_result_id_str+=str(i)+" "

    ## 取得基金全名
    cur_NameList = conn.cursor(buffered=True)
    sql = "select a.etf_id,b.etfname "
    sql += "from etf_risk_profit_rank as a "
    sql += "left join just_raw_name_us as b "
    sql += "on a.etf_id= b.etf_id "
    sql += "where a.date="+ str(select_day) +" and a.timeinterval=780 and("
    for i in sorted_fund_result_id:
        sql += "(a.etf_id=\'"+str(i)+"\')or"

    sql = sql[:-2]+") order by a.etf_id asc"
    cur_NameList.execute(sql)
    fund_result_name_str = ""
    for i in cur_NameList.fetchall():
        fund_result_name_str+=str(i[1])+"||"

    ## 權重處理
    weights_str = ""
    for i in weights:
        weights_str+=str(100*(round(float(i), 4)))+" "

    ## 年化收益
    #  開放至三月底，往後取三個月回測做年化
    sql = "select close,etf_id,date from etf_risk_profit_rank where timeinterval=20 and ("
    for i in range(0, len(fund_result_id)):
        sql = sql + "(etf_id=\'" + str(fund_result_id[i]) + "\')or"
    sql = sql[:-2] + ") and ("
    for j in range(0, 2):
        sql = sql + "(date=" + str(select_day + 65*j) + ")or"
    sql = sql[:-2] + ") order by date asc,etf_id asc"
    cur.execute(sql)
    close_arr = []
    for each in cur.fetchall():
        close_arr.append(float(each[0]))
    return_vec = np.array(close_arr).reshape((-1, len(fund_result_id)))
    weights_ary = []
    for i in weights:
        weights_ary.append(float(i))
    expected_return = np.sum(np.multiply(weights_ary,return_vec[0]))
    after3month = np.sum(np.multiply(weights_ary,return_vec[1]))
    annual_retrun_rate = 4*(after3month-expected_return)/expected_return
    annual_retrun_rate = 100*(round(float(annual_retrun_rate), 3))

    ##清空stderr
    #sys.stderr = stderr
    #sys.stdout = stdout

    netvalue = ""
    netvalue_3m = ""
    for i in return_vec[0]:
        netvalue += str(i)+" "
    for j in return_vec[1]:
        netvalue_3m += str(j)+" "


    #print("iV"+str(fig_png)+"=")
    print(str(fig_png))
    print(fund_result_id_str)
    print(fund_result_name_str[:-2])
    print(weights_str)
    print(annual_retrun_rate)
    print(expected_return)
    print(netvalue)
    print(netvalue_3m)

def get_working_days(start_date, end_date):
    from dateutil import rrule
    return len(list(rrule.rrule(rrule.DAILY, byweekday=range(0, 5), dtstart=start_date, until=end_date)))

if __name__ == "__main__":
    main(sys.argv[1])


    
