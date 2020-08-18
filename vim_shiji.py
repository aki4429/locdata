#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import subprocess
import datetime

def vim_shiji(num, koshinbi):
    files = os.listdir('locshiji')
    pfiles =[]
    for filename in files:
        if filename.startswith('shiji') and filename.endswith('.csv'):
            #ファイル名から、日付を取り出し。
            day = datetime.datetime.strptime(filename, 'shiji%Y-%m-%d.csv')
            #更新日より大きいものだけ
            if day > koshinbi :
                pfiles.append(filename)

    line =''
    for i, f in enumerate(pfiles[:num]) : #最初のnum行のみスライスして
        line += '\n ' + str(i+1) + ')' + f 

    vim =''
    if os.path.isfile('/usr/bin/gvim') :
        print('/isr/bin/gvim はあります。')
        vim = 'gvim'
    else:
        print('/isr/bin/gvim はありません。')
        vim = 'gvim.exe'

    res = ''
    while res !='q' :
        print(line)
        print('*'*20)
        res = input('表示するファイルを選んでください。(終了=q):')
        if res != 'q':
            result = subprocess.run((vim, os.path.join('locshiji', pfiles[int(res)-1])))
