#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#code:
#:8=model, 8:11=spec, 11:17=piece, 20:24=legcolor, 24:31=fab1, 31:39=fab2
#39:40=toku

import glob
import csv
import datetime as dt
import copy

#番地リスト読み込み外部モジュール
#from dbread import Loc, session
import bread

#更新日読み込み
def read_koshin():
    with open('koshinbi.txt') as f:
        koshinbi = s2d(f.read().strip())

    return koshinbi


#番地リスト読み込み
def read_banch(hiduke):
    bdata = bread.read_banch(hiduke)
    return bdata

shijiname = glob.glob('./shiji/*.csv')[-1]

#生産計画データ
sdata = [] 

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
    elif 'CH271' in model and (piece != '35' and piece != '37') :
        model = "013" + model + 'I'
    elif 'CH232-35' in model :
        model = model.replace('CH232-35', 'CH232W-35')
    elif 'CH232-37' in model :
        model = model.replace('CH232-37', 'CH232W-37')
    else:
        model = "013" + model 

    return model + "-" + piece + "C " + fab1


def read_shiji_file(shijiname):
    sdata=[]
    #shiyo 製品コード1 製番4 納期5 指示数6 
    #shiji 規格23 製番55 製造開始日27 製品数 35 担当者13　=8205:検査
    #CH232とCH271の国産(N/NN)以外で、バイオーダー(Z)でないもの
    with open( shijiname, encoding='CP932') as f:
        reader = csv.reader(f)
        for row in reader:
            if (row[13]=="8205" and row[23][8:11].strip() != "N" and row[23][8:11] != "NN" ) and  ('CH232' in row[23][:8].strip() or 'CH271' in row[23][:8]) and  row[23][39:40] != "Z":
                sdata.append([repl(row[23]), row[55], s2d(row[27]), row[35]])

    return sdata

def make_models(sdata):
    models = {}
    #モデル別の情報
    for row in sdata:
        if row[0] in models:
            models[row[0]].append([row[1], row[2], row[3]])
        else:
            models[row[0]] = []
            models[row[0]].append([row[1], row[2], row[3]])

    return models

def get_dates(sdata):
#日付別の情報
#shiji 規格23 製番55 製造開始日27 製品数 35 担当者13　=8205:検査
    dates = {}
    for row in sdata:
        if row[2] not in dates:
            dates[row[2]] = []
            #コード、製番、数量 のリスト
            dates[row[2]].append([row[0], row[1], row[3]])
        else:
            dates[row[2]].append([row[0], row[1], row[3]])

    return dates

#日付のリスト
def get_days(dates, koshinbi):
    odays = sorted(dates)
    days = []
    for d in odays:
        if d > koshinbi:
            days.append(d)

    return days

#for d in days:
#    print(d.strftime('%m/%d') +":")
#    for v in dates[d]:
#        print(v)

#class Shiji:
#    def __init__(self, seiban, code, ):

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

def print_days(days):
    i = 0
    line =""
    for d in days:
        if i < 10 :
            line += str(i+1) + ")"
            line += d.strftime('%m/%d ')
            i += 1

    print(line)

#日付をキーにして、コードと使用総数のリストと使用番地指示。
#(参考) dates = key = 日付 + v = コード、製番、数量 のリスト 辞書
#codes =  コード, 数量の辞書をつくつ
def loc_shiji(bdata, days, dates, j):
    shiji_days={}
    dc_bdata = copy.deepcopy(bdata)
    i=0
    for d in days:
        line = ''
        if i < j :
            shiji_days[d] = []
            line += '\n' + d.strftime('%m/%d') +" 計画分 TFC縫製カバー使用番地: "
            line += '\n=================================='
            codes = {}
            for v in dates[d]:
                if v[0] not in codes:
                    codes[v[0]] = int(v[2])
                else:
                    codes[v[0]] += int(v[2])

            sorted_codes = sorted(codes.items())

            for k, val in sorted_codes:
                line += '\n' + k+'('+str(val)+')'+'は、'
                counter = 0
                for shi in shiji(k, int(val), dc_bdata):
                    if counter > 0: #指示が2行目からは行頭にスペースを
                        line += '\n' + ' '*25 
                    line += '['+shi[0]+']' +'(' + str(shi[1]) +')から'+ '[' + str(shi[2]) + ']を使用してください。'  
                    counter += 1

            line += '\n-------------------------------------'
            line += '\nコード (数量)  [製番]'
            for data in dates[d]:
                line += '\n'+ data[0] + '(' + data[2] + ') ' + '[' + data[1] +']'

            print(line)
            shiji_days[d].append(line)

            i += 1

    return shiji_days

#モデル別受注数辞書作成

def juchu_su(models, koshinbi):
    juchu_q = {}  #受注数量

    #models辞書のキー(モデル名)をリストで
    model_names = sorted(models)

    for name in model_names:
        total = 0
        for line in models[name]:
            if line[1] > koshinbi :
                total += int(line[2])

        juchu_q[name] = total

    return juchu_q

    
#モデル別在庫数辞書作成

def zaiko_su(bdata):
    zaiko_q = {}  #在庫数量
    for row in bdata:
        if row[1] in zaiko_q:
            zaiko_q[row[1]] += row[2]
        else:
            zaiko_q[row[1]] = row[2]

    del zaiko_q['empty']

    return zaiko_q

#print(zaiko_q)

#カバー在庫・受注数リストの作成

def write_cover_zaiko(zaiko_q, juchu_q):
    cover_z =[]

    for k, v in zaiko_q.items():
        cover_z.append([k, v, 0])

    for k, v in juchu_q.items():
        flag = 0
        for row in cover_z:
            if k == row[0]:
                row[2] = v
                flag = 1

        if flag == 0:
            cover_z.append([ k, 0, v ])

    cover_z.sort()

    with open('cover_zaiko.csv', 'w', encoding='CP932') as f:
        writer = csv.writer(f)
        writer.writerows(cover_z)

    print('cover_zaiko.csv を書きだしました。')


def get_shiji(i):
    koshinbi = read_koshin()
    bdb = read_banch(koshinbi)
    print(shijiname)
    sdb = read_shiji_file(shijiname)
    dates = get_dates(sdb)
    print(koshinbi)
    days = get_days(dates, koshinbi)
    shiji_days = loc_shiji(bdb, days, dates, i)
    return shiji_days


def write_shiji(shiji_days):
    for d, v in shiji_days.items():
        filename = 'locshiji/shiji' + d.strftime('%Y-%m-%d') + '.csv'
        with open(filename, 'w', encoding='CP932') as f:
            f.writelines(v)

def write_stock(hiduke, bdb):
    filename = 'stock/stock_' + hiduke.strftime('%Y%m%d') + '.csv'
    with open(filename, 'w', encoding='CP932') as f:
        writer = csv.writer(f)
        writer.writerows(bdb)

#日付をキーにして、コードと使用総数のリストと使用番地指示。
#(参考) dates = key = 日付 + v = コード、製番、数量 のリスト 辞書
#codes =  コード, 数量の辞書をつくつ
def koshin(bdata, days, dates):
    for d in days:
        line = ''
        line += '\n' + d.strftime('%m/%d') +" 計画分 TFC縫製カバー使用番地: "
        line += '\n=================================='
        codes = {} #コード数量のリストを作成
        for v in dates[d]:
            if v[0] not in codes:
                codes[v[0]] = int(v[2])
            else:
                codes[v[0]] += int(v[2])

        sorted_codes = sorted(codes.items())

        for k, val in sorted_codes:
            line += '\n' + k+'('+str(val)+')'+'は、'
            counter = 0
            for shi in shiji(k, int(val), bdata):
                if counter > 0:
                    line += '\n' + ' '*25 
                line += '['+shi[0]+']' +'(' + str(shi[1]) +')から'+ '[' + str(shi[2]) + ']を使用してください。'  
                counter += 1

        line += '\n-------------------------------------'
        line += '\nコード (数量)  [製番]'
        for data in dates[d]:
            line += '\n'+ data[0] + '(' + data[2] + ') ' + '[' + data[1] +']'

        print(line)

        write_stock(d, bdata)

    return bdata


def make_koshin():
    koshinbi = read_koshin()
    bdb = read_banch(koshinbi)
    print('製造指示書：', shijiname, 'を読み込みました。')
    sdb = read_shiji_file(shijiname)
    dates = get_dates(sdb)
    print('更新日：', koshinbi.strftime('%Y/%m/%d'))
    days = get_days(dates, koshinbi)
    print('-'*20)
    print_days(days)
    suji = int(input('更新する日を数字で選んでください。:'))
    kos = days[:suji]
    print_days(kos)
    res = input('上記の日付を更新してもよいですか(y/n):')
    if res == 'y':
        koshin(bdb, kos, dates )
        with open('koshinbi.txt', 'w') as w:
            koshin_date= kos[-1].strftime('%Y/%m/%d')
            w.write(koshin_date)
        
        print('更新日を' + koshin_date + 'に変更しました。')
    else:
        print('更新を中止しました。')


def write_cover():
    koshinbi = read_koshin()
    print('更新日は' + koshinbi.strftime('%Y/%m/%d') + 'です。')
    bdb = read_banch(koshinbi)
    print('製造指示書：', shijiname, 'を読み込みました。')
    sdb = read_shiji_file(shijiname)
    models = make_models(sdb)
    write_cover_zaiko(zaiko_su(bdb), juchu_su(models, koshinbi))

#write_shiji(get_shiji(5))
#sdb = read_shiji_file(shijiname)
#dates = get_dates(sdb)
#koshinbi = read_koshin()
#make_koshin()

#write_cover()

def make_cover_zaiko():
    koshinbi = read_koshin()
    bdb = read_banch(koshinbi)
    print(shijiname)
    sdb = read_shiji_file(shijiname)
    models = make_models(snd)
    print(koshinbi)

    write_cover_zaiko(zaiko_su(bdb), juchu_su(models, koshinbi)):



