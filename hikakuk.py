#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import csv

qdata =[]

with open('cover_zaiko_9obic.csv') as f:
    reader = csv.reader(f)
    for row in reader:
        qdata.append(row)

ndata =[]

with open('cover_zaiko.csv') as f:
    reader = csv.reader(f)
    for row in reader:
        ndata.append(row)

result =[]
for qline in qdata:
    for  nline in ndata:
        if qline[0] == nline[0] and int(nline[2]) > int(qline[2]) :
            result.append([nline[0], qline[2], nline[2]])

with open('result.csv', 'w') as f:
    writer = csv.writer(f)
    writer.writerows(result)


