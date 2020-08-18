# vim:fileencoding=utf-8

"""
同じアイテムを見つけ、一緒になったとき、maxを超えないか
チェック。超えなければ、小さい数の方を大きいあ数の箱へ
移動するプランを提案。
全部で、何箱空き箱にできるか表示
"""

#在庫を読む
import csv
import os
import glob
import itertools
import copy

#ファイル名を指定
filelist = sorted(glob.glob('stock/stock*.csv'), key=lambda f: os.stat(f).st_mtime, reverse=True)
ans = input("ファイルは{}でいいですか?:".format(filelist[0]))
if ans != 'n':
    filename = filelist[0]

print('filename', filename)
#maxlist を読む
maxlist = []
with open('maxlist.csv') as f:
    reader = csv.reader(f)
    for row in reader:
        maxlist.append(row)

#stock データを読む
stock_data = []
def stock_read(filename):
    with open(filename, encoding='CP932') as f:
        reader = csv.reader(f)
        for row in reader:
            stock_data.append(row)

stock_read(filename)

#すべてのアイテムを取り出してユニークなリスト
allitem = []
for row in stock_data:
    allitem.append(row[1])

allitem = list(set(allitem))
allitem.remove('empty')
#print('allitem', allitem)
#print('stock_data', stock_data)

def get_max(code:str, maxlist:list)->int:
    for d in maxlist:
        if d[0] == code.split('-')[1][:2]:
            return int(d[1])


#組み合わせで、統一できるかチェックして
#できれば、統一案をはきだす。
def teian(items:list, itemname:str)->list:
    #items = copy.deepcopy(items)
    ido = []
    #最初にそのアイテムのmaxを取得する。
    #print('itemname:',itemname)
    max_v = get_max(itemname, maxlist)
    #print('max_v', max_v)
    kumiawase = [] #組み合わせの総当り収納
    kumiawase += itertools.combinations(items, 2)

    kumilist = [] #組み合わせはtupleなのでlistへ変換
    for kumi in kumiawase:
        kumilist.append(list(kumi))

    #print('kumilist', kumilist)
    #print('len(kumilist)', len(kumilist))
    for b in kumilist:
        #print('b[0][1]', b[0][1])
        #print('b[1][1]', b[1][1])
        if int(b[0][1]) + int(b[1][1]) <= max_v \
            and (int(b[0][1]) != 0 and int(b[1][1]) != 0):
            ido.append(copy.deepcopy([b[1], b[0], itemname]))
            print('{0}({1})から, {2}({3})へ{4} : {5} 移動'.format(\
		b[1][0], b[1][1], b[0][0], b[0][1], b[1][1],itemname))
            b[0][1] = int(b[1][1]) + int(b[0][1])
            b[1][1] = 0

    return ido

ido = []
for item in allitem:
    items =[]
    for data in stock_data:
        if data[1] == item:
            items.append([data[0], data[2]]) #番地数量だけのリストに

    if len(items) > 1 : #同じ品名のデータが2つ以上ある場合
    	#print('items', items)
    	#print('items[0][1]', items[0][1])
    	ido.append(teian(items, item)) 

#print(ido)	

