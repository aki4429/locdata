#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sqlite3
import pandas as pd
import pandas.io.sql as psql
import csv
import shutil

DBN = 'locdata.sqlite'
DB = '../odachin.pythonanywhere.com/db.sqlite3'

def read_locdata_2():
    conn = sqlite3.connect(DBN)
    #cur = conn.cursor()

    bdf = psql.read_sql("SELECT * FROM locdata;", conn)
    conn.close()

    #列名インデックスは無視して変換
    bdb = bdf.values.tolist()
    print(DBN, "の locdata テーブルを読み込みました。")
    return bdb

def read_locdata():
    conn = sqlite3.connect(DB)
    cur = conn.cursor()

    bdf = cur.execute("SELECT banch, code, qty FROM locdata;")

    #tuple でとりだし、list に変換
    data=[]
    bdb = bdf.fetchall()
    for row in bdb:
        data.append(list(row))

    conn.close()
    print(DB, "の locdata テーブルを読み込みました。")
    return data

def save_locdata(d):
    bdb = read_locdata()
    filename = 'stock/stock_' + d.strftime('%Y%m%d') + '.csv'
    shutil.copy(filename, filename+'.bk')
    with open(filename, 'w', encoding='CP932') as f:
        writer = csv.writer(f)
        writer.writerows(bdb)

    print(filename, 'を更新しました。')
