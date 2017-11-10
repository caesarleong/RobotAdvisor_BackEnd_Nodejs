# -*- coding: utf-8 -*-
#!/usr/bin/env python3
"""
Created on Tue Feb 28 23:12:36 2017

@author: user
"""

import numpy as np
from numba import jit, autojit,int32,cuda

class CovCor:
    def __init__(self,TheDay,timeinterval):#TheDay為date格式，timeinterval為string格式
        self.timeinterval = timeinterval
        self.TheDay = TheDay
        
    #@jit(int32[:](int32[:]))
    @jit(nogil = True,nopython = False)
    def cov_jit(self,x):
        return np.cov(x)
    
    #@jit(int32[:](int32[:]))
    @jit(nogil = True,nopython = False) #用Ture會有錯誤訊息，代表吃不了cov這樣比較高級的函式
    def corrcoef_jit(self,x):
        return np.corrcoef(x)
