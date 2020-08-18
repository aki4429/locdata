#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import csv

EFN = './data/empty_rack.csv' # empty file name

def get_empty(bdata):
    empties = []
    for row in bdata:
        if row[2] == 0 : #数量がゼロの時
            empties.append(row)

    return empties

def write_empty(bdata):
    with open(EFN, 'w', encoding='CP932') as f:
        writer = csv.writer(f)
        writer.writerows(get_empty(bdata))
        print(EFN, 'を書き出しました。')
