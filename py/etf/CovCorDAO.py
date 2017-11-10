# -*- coding: utf-8 -*-
#!/usr/bin/env python3
"""
Created on Mon Feb 27 23:00:05 2017

@author: user
"""
import time
from numba import jit, autojit,int32,cuda
class CovCorDAO:
    def CreateTable(self,conn):
        cur = conn.cursor()
        
        cur.execute('''CREATE TABLE CovCorTest2(
                           fund VARCHAR(64),
                           date VARCHAR(64),
                           timeinterval VARCHAR(5),
                           covcor INTEGER,
                           value FLOAT[]
                    )'''
        )
        
    def DropTable(self,conn):
        cur = conn.cursor()
        cur.execute("DROP TABLE CovCorTest2")    
        
    @jit
    def LoadFund(self,conn, FundNames):
        cur = conn.cursor()
        cur.execute("SELECT fund_id,workday_net_worth FROM fund_net_worth_array %s ORDER BY fund_id "%(FundNames))
        return cur.fetchall()
        #for num in cur.fetchall() :
         #   print(num)
    
    @jit
    def LoadFundOld(self,conn):
        cur = conn.cursor()
        cur.execute("SELECT fundname,workday_net_worth FROM fund_net_worth ORDER BY fundname ")
        return cur.fetchall()
    
    @jit
    def InsertData(self,conn, Array):
        cur = conn.cursor()
        cur.executemany("""INSERT INTO CovCorTest2(fund,date,timeinterval,covcor,value)
        VALUES (%s,%s,%s,%s,%s)""",Array
        )
        
    def Insert(self,conn,fund,date,timeinterval,covcor,value):
        cur = conn.cursor()
        cur.execute("""INSERT INTO CovCorTest2(fund,date,timeinterval,covcor,value) 
        VALUES(%s,%s,%s,%s,%s)""", (fund,date,timeinterval,covcor,value))
        
    def WriteFile(self,FileName,DataArray):
        #f = open('CovCorData.txt', 'w')
        with open(FileName,'w') as f: #用with的寫法，用完會即關
            for data in DataArray:
                f.write(str(data)+"\n")
