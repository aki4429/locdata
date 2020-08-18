#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#TFC輸入カバーを管理するクラス
#更新日読み込み、
#製造指示書読み込み
#番地リスト読み込み

import glob
import csv
import datetime as dt
import copy
import readline

#番地リスト読み込み外部モジュール
#from dbread import Loc, session
from bread import read_banch, read_rev_banch
from dbread import read_locdata

#更新日読み込み
from read_koshin import read_koshin

#製造指示ファイル読み込み
#shiji 規格23 製番55 製造開始日27 製品数 35 担当者13　=8205:検査
from read_shiji import read_shiji

#ロケーション指示を作成
from loc_shiji import write_shiji

#更新
from koshin import koshin, write_stock, write_racklist

#cover_zaiko.csv 書き出し
from make_cover_zaiko import make_cover_zaiko

#ロケーション指示をvimで参照
from vim_shiji import vim_shiji

#empty ラック書き出し
import get_empty

#インボイスデータ選択
import choose_inv

#カバー整理場所作成
import make_seiri

#ラベル用データ書き出し
import make_label

class TfcCover:
    def __init__(self):
        self.koshinbi = read_koshin()
        print('更新日は' + self.koshinbi.strftime('%Y/%m/%d') + 'です。')
        #self.bdata = read_banch(self.koshinbi)
        self.bdata = read_locdata()
        self.sdata = read_shiji()
        self.models = self.make_models()
        self.dates = self.get_dates(self.sdata)
        self.days = self.get_days(self.dates, self.koshinbi)

    def print_banch(self):
        print(self.sdata)

    def make_models(self):
        models = {}
        #モデル別の情報
        for row in self.sdata:
            if row[0] in models:
                models[row[0]].append([row[1], row[2], row[3]])
            else:
                models[row[0]] = []
                models[row[0]].append([row[1], row[2], row[3]])

        return models


    def get_dates(self,sdata):
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
    def get_days(self, dates, koshinbi):
        odays = sorted(dates)
        days = []
        for d in odays:
            if d > koshinbi:
                days.append(d)

        return days

    def search_code(self):
        res = ''
        while(res != 'q'):
            res = input('検索コードを入力してください。')
            for row in self.bdata:
                if res in row[1]:
                    print(row)

    def search_banch(self):
        res = ''
        while(res != 'q'):
            res = input('検索番地を入力してください。')
            for row in self.bdata:
                if res in row[0]:
                    print(row)

    def print_days(self, days):
        i = 0
        line =""
        for d in days:
            if i < 10 :
                line += str(i+1) + ")"
                line += d.strftime('%m/%d ')
                i += 1

        print(line)


    def make_shiji(self):
        write_shiji(self.bdata, self.sdata, self.dates, self.days,self.koshinbi)

    def make_koshin(self):
        self.print_days(self.days)
        suji = int(input('更新する日を数字で選んでください。:'))
        kos = self.days[:suji]
        self.print_days(kos)
        res = input('上記の日付を更新してもよいですか(y/n):')
        if res == 'y':
            koshin(self.bdata, kos, self.dates )
            with open('koshinbi.txt', 'w') as w:
                koshin_date= kos[-1].strftime('%Y/%m/%d')
                w.write(koshin_date)

            print('更新日を' + koshin_date + 'に変更しました。')
        else:
            print('更新を中止しました。')

    def save(self):
        write_stock(self.koshinbi, self.bdata)

    def write_cover_zaiko(self):
        make_cover_zaiko(self.models, self.koshinbi, self.bdata)

    def show_shiji(self):
        #表示ファイル数を指定してロケーション指示ファイルを参照
        num = input('表示するファイル数を指定してください。return=5:')
        if num == '':
            num = 5
        else:
            num = int(num)

        vim_shiji(num, self.koshinbi)

    def reload(self) :
        self.bdata = read_rev_banch()

    def write_empty(self):
        get_empty.write_empty(self.bdata)

    def write_inv(self):
        get_empty.write_empty(self.bdata)
        arrivedfile, t_data = choose_inv.write_c(self.bdata)
        m=make_seiri.MakeSeiri(arrivedfile, t_data)
        make_label.write(m.lines, m.af)
        m.write_kn(self.bdata, self.koshinbi)

    def write_rack(self):
        write_racklist(self.bdata, self.koshinbi)
        
        



#tc = TfcCover()
#tc.get_shiji()
#tc.search()
#tc.make_shiji()
#tc.make_koshin()
#tc.show_shiji()
