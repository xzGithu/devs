# coding:utf-8
# @Time     :2020/3/25 13:43
# @Author   :Xu Zhe
# @Email    :mistest163@163.com
# @File     :views-stu.py

# -*- coding: utf-8 -*-
from transitions import Machine
#先定义一个类
class Work(object):
    pass

model=Work()
#定义状态
states=['1','2','0']
#定义状态转移
transitions=[
    {'trigger':'start','source':['1','2'],'dest':'1'},
    {'trigger':'pause','source':'1','dest':'2'},
    {'trigger':'stop','source':['1','2'],'dest':'0'}
]
#初始化状态机
machine = Machine(model=model, states=states, transitions=transitions, initial='1')
#根据输入的命令转换状态
while True:
    print '当前状态：',model.state
    command = raw_input("请输入指令：")
    if command=='1':
        model.start()
        print '改变后状态：', model.state,'\n'
    elif command=='2':
        model.pause()
        print '改变后状态：', model.state,'\n'
    elif command=='0':
        model.stop()
        print '改变后状态：', model.state,'\n'
        break
    else:
        print "指令输入错误\n"
