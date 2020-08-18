#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sqlite3
import csv
import os
from datetime import date,timedelta

DB_FILE = 'tfc.sqlite'

#データベースから南濃いきで、在庫区分1の基準日以降のデータを取り出し。
#取り込み日、ETD、INV NO、hコード、数量
def db_connect():
    con = sqlite3.connect(DB_FILE)
    cur = con.cursor()

    begin_day = date.today() - timedelta(weeks=4) #２週間前以降のデータ取得
    begin_day =  begin_day.strftime('%Y-%m-%d')

    #cur.execute("select i.delivery, i.etd, i.invn, c.hcode, v.qty from ((((poline o inner join invline v on v.poline_id = o.id) inner join po p on o.po_id = p.id) inner join inv i on v.inv_id = i.id) inner join tfc_code c on c.id = v.code_id) where i.delivery > ? and p.comment = 'To Hukla Japan/Nanno ' and c.zaiko=1", (begin_day,))

    cur.execute("select i.delivery, i.etd, i.invn, c.hcode, v.qty from ((invline v inner join inv i on v.inv_id = i.id) inner join tfc_code c on c.id = v.code_id) where i.delivery > ?  and c.zaiko=1", (begin_day,))
    invlines = cur.fetchall()

    cur.close()
    con.close()

    return invlines

#CH2で始まるカバーコードのみに限定
def cov_data():
    covers = []
    invlines = db_connect()
    for row in invlines:
        if row[3].startswith('013CH2') :
            covers.append(list(row))

    return covers

def inv_select():
    covers = cov_data()
    #メニュー用にデータを取り出す。取り込み日、ETD, inv no
    inv_data = set()
    for row in covers:
        inv_data.add((row[0], row[1], row[2]))

    idata = list(inv_data)
    idata.sort()
    print('南濃取り込み/ETD/INV#')
    print('-'*20)
    for i, row in enumerate(idata):
        print(i,")", *row)

    print('-'*20)
    ans = int(input('コンテナを選んでください。'))

    #該当するインボイスのコード、数量を取り出し。
    c_data = []
    inv_n = idata[ans][2]
    for row in covers:
        if row[2] ==  inv_n :
            c_data.append([row[3], row[4]])

    #入荷カバー書込みファイル名
    arrivedfile = idata[ans][0] + idata[ans][2]
    arrivedfile = arrivedfile.replace('-', '')

    #重複コードは加算して一つに
    sumdata={}
    for data in c_data :
        if data[0] in sumdata:
            sumdata[data[0]] += int(data[1])
        else:
            sumdata[data[0]] = int(data[1])

    t_data =[] #code, qty の配列
    for k, v in sumdata.items():
        t_data.append([k, v])

    t_data.sort()

    return arrivedfile, t_data

def write_c(bdata):
    arrivedfile, t_data = inv_select()
    full_name = os.path.join('data', arrivedfile + '.csv')
    with open(full_name, 'w', encoding='CP932') as f:
        writer = csv.writer(f)
        writer.writerows(t_data)

    print(full_name, 'を書きました。')

    #到着リストで、コードが同じときラックのデータを追記
    add_data = []
    for td in t_data:
        for bd in bdata:
            if td[0] == bd[1]:
                td.extend([bd[0], bd[2]])

    #full_name = os.path.join('data', arrivedfile + 'out.csv')
    #with open(full_name, 'w', encoding='CP932') as f:
    #    writer = csv.writer(f)
    #    writer.writerows(t_data)

    #print(full_name, 'を書きました。')

    return arrivedfile, t_data



#write_c()
