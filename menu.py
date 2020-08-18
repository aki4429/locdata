#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#TFC輸入カバーのメニュー

from tfc_cover import TfcCover

tc = TfcCover()

menu_line =""" 
1)検索コード
2)検索番地
3)ロケーション指示 (output)
4)ロケーション指示 (表示/印刷)
5)更新
6)cover_zaiko.csv 書き出し (在庫報告用)
7)修正データ読み込み(stockフォルダのrevから始まるファイル)
8)保存
9)emptyラック書き出し(data/empty_rack.csv)
10)到着インボイスデータ選択/加工
11)棚卸し用リスト打ち出し(racklist)
"""

ans = ''
while ans != 'q':
    print(menu_line)
    ans = input('メニューを選んでください。(q=終了)')
    if ans == '1':
        tc.search_code()
    elif ans == '2':
        tc.search_banch()
    elif ans == '3':
        tc.make_shiji()
    elif ans == '4':
        tc.show_shiji()
    elif ans == '5':
        tc.make_koshin()
    elif ans == '6':
        tc.write_cover_zaiko()
    elif ans == '7':
        tc.reload()
    elif ans == '8':
        tc.save()
    elif ans == '9':
        tc.write_empty()
    elif ans == '10':
        tc.write_inv()
    elif ans == '11':
        tc.write_rack()

