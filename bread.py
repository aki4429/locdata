#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import csv
import glob
import datetime
import glob

SPATH = './stock/rev*.csv'

def read_banch(d):
    filename = './stock/stock_' + d.strftime('%Y%m%d') + '.csv'
    print(filename, "を読み込みました。")

    data = []

    with open(filename, encoding='CP932') as f:
        reader = csv.reader(f)
        for row in reader:
            data.append([row[0], row[1], int(float(row[2]))])

    data.sort()
    return data

def read_rev_banch():
    rfiles = glob.glob(SPATH)
    for i, rf in enumerate(rfiles) :
        print(i, ')', rf)

    ans = int(input('読み込むファイルを選んでください。'))

    filename = rfiles[ans]
    print(filename, "を読み込みます。")

    data = []

    with open(filename, encoding='CP932') as f:
        reader = csv.reader(f)
        for row in reader:
            data.append([row[0], row[1], int(float(row[2]))])

    data.sort()

    return data


