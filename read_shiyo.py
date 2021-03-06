#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#code:
#:8=model, 8:11=spec, 11:17=piece, 20:24=legcolor, 24:31=fab1, 31:39=fab2
#39:40=toku

import glob
import csv
import datetime as dt

from dbread import Loc, session

shiyoname = glob.glob('./shiyo/*.csv')[0]

data = [] 

#納期は'yyyy/mm/dd'形式なので、/でスプリットして、int()で数のリストを作成
#datetime形式に変換
def s2d(hiduke):
    hlist = hiduke.split('/')
    hlist = [int(x) for x in hlist]
    return dt.datetime(*hlist)

#縫製品カバーコードに変換
def repl(code):
    model = code[:8].strip()
    piece = code[11:17].strip()
    fab1 = code[24:31].strip()
    #CH232で35,37で無い場合
    if 'CH232' in model and piece != '35' and piece != '37' :
        model = "013" + model + 'WI'
    elif 'CH232' in model and (piece == '35' or piece == '37') :
        model = "013" + model + 'W'
    elif 'CH271' in model and (piece != '35' or piece != '37') :
        model = "013" + model + 'I'
    else:
        model = "013" + model 

    return model + "-" + piece + "C " + fab1


#shiyo 製品コード1 製番4 納期5 指示数6 
#CH232とCH271の国産(N/NN)以外で、バイオーダー(Z)でないもの
with open( shiyoname, encoding='CP932') as f:
    reader = csv.reader(f)
    for row in reader:
        if (row[1][8:11].strip() != "N" and row[1][8:11].strip() != "NN" and row[1][8:11].strip() != "NE" ) and  ('CH232' in row[1][:8].strip() or 'CH271' in row[1][:8].strip()) and  row[1][39:40] != "Z":
            data.append([repl(row[1]), row[4], s2d(row[5]), row[6]])

#モデル別の情報
models = {}
model = ""
for row in data:
    if model in models:

        models[row[0]].append([row[1], row[2], row[3]])
        model = row[0]
    else:
        models[row[0]] = []
        models[row[0]].append([row[1], row[2], row[3]])

#日付別の情報
#shiyo 製品コード1 製番4 納期5 指示数6 
dates = {}
for row in data:
    if row[2] not in dates:
        dates[row[2]] = []
        dates[row[2]].append([row[0], row[1], row[3]])
    else:
        dates[row[2]].append([row[0], row[1], row[3]])

#日付のリスト
days = sorted(dates)

for d in days:
    print(d.strftime('%m/%d') +":")
    print(dates[d])

class Shiji:
    def __init__(self, seiban, code, ):



