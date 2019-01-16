#! -*- coding:utf-8 -*-
dic1=[{'nick': '无忌', 'flag': 8389120, 'uin': 1609796341, 'face': 108}, {'nick': '逍遥一生', 'flag': 582, 'uin': 3646335671, 'face': 591}, {'nick': '第一', 'flag': 298320448, 'uin': 1095428490, 'face': 522}, {'nick': 'わ\xa0た\xa0し', 'flag': 289440256, 'uin': 2025254517, 'face': 528}]

for i in dic1:
    if i["uin"]==1609796341:
        print i["nick"]