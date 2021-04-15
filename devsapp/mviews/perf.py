#coding:utf-8
from django.contrib.auth.decorators import login_required
import MySQLdb
from django.shortcuts import render
import time
import sqlite3
from devsapp.forms import query_form

@login_required
def gethostper(request):
    times = []
    values = []
    times1 = []
    values1 = []
    times2 = []
    values2 = []
    metricname=""
    if request.method == "POST":
        form = query_form(request.POST)
        ip = request.POST.get("hostip")
        metric = request.POST.get("metric")
        # print(form)
        # if form.is_valid():
        # ip = form.cleaned_data['hostip']
        # metric = form.cleaned_data['metric']
        print(ip, metric)
        if str(metric) == "cpu_usage":
            metricname = "CPU"
        else:
            metricname = "Memory"
        print(metricname)
        # print(ip, metric)
        sql = "SELECT clock, value FROM devsapp_history_uint where itemid='"+str(metric)+"' and endpoint='"+str(ip)+"' LIMIT 30"
        print(sql)
        connect = sqlite3.connect("D:/py-source/devs/db.sqlite3")
        # connect=MySQLdb.connect(host="192.168.182.179",user="root",passwd="",db="zabbix",port=3306)
        cursor = connect.cursor()
        cursor.execute(
            "SELECT clock, value FROM devsapp_history_uint where itemid='cpu_usage' and endpoint='127.0.0.1'  LIMIT 100")
        # cursor.execute("select clock,value from history_uint where itemid=27421 limit 100")
        datas = cursor.fetchall()
        cursor.execute(
            "SELECT clock, value FROM devsapp_history_uint where itemid='mem_usage' and endpoint='127.0.0.1'  LIMIT 100")
        datas1 = cursor.fetchall()
        cursor.execute(sql
            )
        datas2 = cursor.fetchall()
        times = []
        values = []
        times1 = []
        values1 = []
        for i in datas:
            # print(i)
            times.append(int(i[0]))
            values.append(int(i[1]))
        for i in datas1:
            # print(i)
            times1.append(int(i[0]))
            values1.append(int(i[1]))
        for i in datas2:
            # print(i)
            times2.append(int(i[0]))
            values2.append(int(i[1]))
        times = [time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(i)) for i in times]
        times1 = [time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(i)) for i in times1]
        # times1=[i for i in range(len(times))]
        return render(request, 'asset/data.html',
                      {"time": times, "value": values, "time1": times1, "value1": values1,"time2":times2,"value2":values2,"mname":metricname, "form": form})
    else:
        form = query_form()
        connect = sqlite3.connect("D:/py-source/devs/db.sqlite3")
        # connect=MySQLdb.connect(host="192.168.182.179",user="root",passwd="",db="zabbix",port=3306)
        cursor = connect.cursor()
        cursor.execute(
            "SELECT clock, value FROM devsapp_history_uint where itemid='cpu_usage' and endpoint='127.0.0.1'  LIMIT 100")
        # cursor.execute("select clock,value from history_uint where itemid=27421 limit 100")
        datas = cursor.fetchall()
        cursor.execute(
            "SELECT clock, value FROM devsapp_history_uint where itemid='mem_usage' and endpoint='127.0.0.1'  LIMIT 100")
        datas1 = cursor.fetchall()

        for i in datas:
            # print(i)
            times.append(int(i[0]))
            values.append(int(i[1]))
        for i in datas1:
            # print(i)
            times1.append(int(i[0]))
            values1.append(int(i[1]))
        times = [time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(i)) for i in times]
        times1 = [time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(i)) for i in times1]
        # times1=[i for i in range(len(times))]
    return render(request, 'asset/data.html',
                      {"time": times, "value": values, "time1": times1, "value1": values1, "form": form})