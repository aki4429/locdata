#!/usr/bin/env python
#coding:utf-8

#TFC縫製品カバーの整理アドレスを設定します。
#yotei_outリストのアイテム毎maxを読み取り、max 毎に分けて
#max箱は新規箱に、max 未満は既存箱と合わせてmax にならない
#場合は、既存箱、既存箱がなければ、新規箱を割り振ります。

import csv
from collections import deque

class Seiri:
    def __init__(self, code, initial_qty, kizons, empties, max_q):
        self.code = code
        self.iqty = initial_qty
        self.kizons = kizons  #該当する既存ケース
        self.empties = deque(empties) #空箱番地
        self.max_q = max_q #箱入れ最大数

    def make_list(self):
        newlines = []
        qty = self.iqty
        while qty > self.max_q :
            poped_empty = self.empties.popleft()
            #print(self.code, self.max_q, poped_empty, 0)
            newlines.append([self.code, self.max_q, poped_empty, 0])
            qty -= self.max_q

        if qty > 0:
            flag = 0
            for case in self.kizons :
                if (qty + case[1] ) <= self.max_q :
                    #print(self.code, qty, case[0], case[1])
                    newlines.append([self.code, qty, case[0], case[1]])
                    flag = 1
                    break

            if flag == 0:
                poped_empty_2 = self.empties.popleft()
                #print(self.code, qty, poped_empty_2, 0)
                newlines.append([self.code, qty, poped_empty_2, 0])

        return newlines
            

