#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import csv
import datetime

#from bread import read_banch
#from read_koshin import read_koshin

#bdata = read_banch(read_koshin())


def drop(bdata):
    uppers = [] #1段目、3段目で数量0でないリスト
    for row in bdata:
        dan = row[0].split('-')[2] 
        if (dan == '1' or dan == '3') and row[2] != 0 :
            uppers.append(row)

    for ue in uppers:
        #2段目、3段目が0のケースを探します。
        shita = ue[0].replace('1', '2').replace('3', '4')
        for data in bdata:
            if data[0] == shita and data[2] == 0:
                #上下の番地を置き換えます。
                data[0] = ue[0]
                ue[0] = shita

    bdata.sort()
    return bdata

#drop(bdata)

#with open('updown.csv', 'w', encoding='CP932') as f:
#    writer = csv.writer(f)
#    writer.writerows(bdata)

