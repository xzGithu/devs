#coding:utf-8
from django.contrib.auth.decorators import login_required
import MySQLdb
from django.shortcuts import render
import time
import sqlite3

@login_required
def gethostper(request):
    connect = sqlite3.connect("D:/py-source/devs/db.sqlite3")
    # connect=MySQLdb.connect(host="192.168.182.179",user="root",passwd="",db="zabbix",port=3306)
    cursor=connect.cursor()
    cursor.execute("SELECT clock, value FROM devsapp_history_uint where itemid='disk_usage' and endpoint='127.0.0.1'  LIMIT 100")
    # cursor.execute("select clock,value from history_uint where itemid=27421 limit 100")
    datas=cursor.fetchall()
    times=[]
    values=[]
    for i in datas:
        # print(i)
        times.append(int(i[0]))
        values.append(int(i[1]))
    times=[time.strftime("%Y-%m-%d %H:%M:%S",time.localtime(i)) for i in times]
    # times1=[i for i in range(len(times))]
    return render(request,'asset/data.html',{"time":times,"value":values})
