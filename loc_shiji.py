#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import copy
from shiji import shiji
from drop import drop

#日付をキーにして、コードと使用総数のリストと使用番地指示。
#(参考) dates = key = 日付 + v = コード、製番、数量 のリスト 辞書
#codes =  コード, 数量の辞書をつくつ
def loc_shiji(bdata, sdata, dates, days, koshinbi, j):
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
            drop(dc_bdata)
            shiji_days[d].append(line)

            i += 1

    return shiji_days

def get_shiji(bdata, sdata, dates, days, koshinbi):
    term = int(input('何日分のピック番地指示をだしますか->?日:'))
    print( term, '日分のピック指示をだします。')
    shiji_days = loc_shiji(bdata, sdata, dates, days, koshinbi, term)

    return shiji_days

def write_shiji(bdata, sdata, dates, days, koshinbi):
    shiji_days = get_shiji(bdata, sdata, dates, days, koshinbi)
    for d, v in shiji_days.items():
        filename = 'locshiji/shiji' + d.strftime('%Y-%m-%d') + '.csv'
        with open(filename, 'w', encoding='CP932') as f:
            f.writelines(v)


