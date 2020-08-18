#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from s2d import s2d


#更新日読み込み
def read_koshin():
    with open('koshinbi.txt') as f:
        koshinbi = s2d(f.read().strip())

    return koshinbi

