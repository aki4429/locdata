#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import copy

def shiji(code, qty, bdb):
    #番地の消費リストを返す
    #bdb は 番地, コード, 数量のリスト
    banches = []
    balance = qty
    for loc in bdb:
        if balance !=0 and loc[1] == code and loc[2] < balance : 
            banches.append([loc[0], loc[2], loc[2]]) 
            #残数を減らします。
            balance = balance - loc[2] 
            #番地DBの数量も減らします。
            loc[2] = 0 #ゼロになる
            loc[1] = 'empty' #emptyにしておかないとゼロでマッチするため
        elif balance != 0 and loc[1] == code and loc[2] == balance: 
            banches.append([loc[0], loc[2], balance]) 
            balance = 0
            #番地DBの数量も減らします。
            loc[2] = 0 #ゼロ
            loc[1] = 'empty'
        elif balance != 0 and loc[1] == code and loc[2] > balance: 
            banches.append([loc[0], loc[2], balance]) 
            #番地DBの数量も減らします。
            loc[2] =loc[2] - balance #残数あり
            balance = 0

    if balance > 0 :
        banches.append(['次の入荷分', '', balance])

    return banches

