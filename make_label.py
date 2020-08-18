#!/usr/bin/env python
# -*- coding: utf-8 -*-

#kizon_new ファイルを読み込んで、=> データを受け取って
#識別ラベル作成用のデータ抽出する。コード、ピース、布地、番地　

#FILENAME = "kizon_new_for_label.csv"
#OUTFILE = "label_data.csv"
HEADDER = ["code", "piece", "fab", "address"]

#項目位置
CODE=0
BANCHI=2
QTY=3

import csv

def kako(lines):
    data = []
    data.append(HEADDER)
    for row in lines:
        if int(float(row[QTY])) == 0:
            line=[]
            item =row[CODE].split("-")[0].replace("013", "")
            piece =row[CODE].split("-")[1].split(" ")[0]
            fab =row[CODE].split("-")[1].split(" ")[1]
            line.append(item)
            line.append(piece)
            line.append(fab)
            line.append(row[BANCHI])
            data.append(line)
            #print(line)
                
    return data

def write(lines, af):
    data = kako(lines)
    filename = "label_data{0}.csv".format(af)
    with open(filename, "w", encoding="CP932") as f:
        writer = csv.writer(f)
        for line in data:
            writer.writerow(line)

    print(filename, 'を書きました。')


#write(OUTFILE, data)
