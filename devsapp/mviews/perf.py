#coding:utf-8
import json
import time

from django.contrib.auth.decorators import login_required
import MySQLdb
from django.shortcuts import render, get_object_or_404
from django.core import serializers
from django.http import HttpResponse
import sqlite3

from devsapp.forms import query_form
from devsapp.models import Items, hosts

@login_required
def gethostper(request):
    times = []
    values = []
    times1 = []
    values1 = []
    times2 = []
    values2 = []
    timesm = []
    valuesm = []
    timesn = []
    valuesn = []
    # hosts = Items.objects.values_list("hostid", flat=True).distinct()
    hostss = hosts.objects.all()
        # values("hostid").distinct()
    print(hostss)
    metricname=""
    connect = sqlite3.connect("D:/py-source/devs/db.sqlite3")
    # connect=MySQLdb.connect(host="192.168.182.179",user="root",passwd="",db="zabbix",port=3306)
    cursor = connect.cursor()
    cursor.execute(
        "SELECT clock, value FROM devsapp_history_uint where itemid_id='cpu_usage' and endpoint='127.0.0.1' order by clock DESC LIMIT 100")
    datas = cursor.fetchall()
    cursor.execute(
        "SELECT clock, value FROM devsapp_history_uint where itemid_id='cpu_usage' and endpoint='192.168.0.1' order by clock DESC LIMIT 100")
    datasn = cursor.fetchall()
    cursor.execute(
        "SELECT clock, value FROM devsapp_history_uint where itemid_id='mem_usage' and endpoint='192.168.0.1' order by clock DESC LIMIT 100")
    # cursor.execute("select clock,value from history_uint where itemid=27421 limit 100")
    datasm = cursor.fetchall()
    cursor.execute(
        "SELECT clock, value FROM devsapp_history_uint where itemid_id='mem_usage' and endpoint='127.0.0.1' order by clock DESC LIMIT 100")
    datas1 = cursor.fetchall()

    for i in datas:
        # print(i)
        times.append(int(i[0]))
        values.append(int(i[1]))
    for i in datas1:
        # print(i)
        times1.append(int(i[0]))
        values1.append(int(i[1]))
    for i in datasm:
        timesm.append(int(i[0]))
        valuesm.append(int(i[1]))
    for i in datasn:
        timesn.append(int(i[0]))
        valuesn.append(int(i[1]))
    times = [time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(i)) for i in times]
    times1 = [time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(i)) for i in times1]
    timesm = [time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(i)) for i in timesm]
    timesn = [time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(i)) for i in timesn]

    if request.method == "POST":
        # form = query_form(request.POST)
        ip = request.POST.get("hostid")
        metric = request.POST.get("itemid")
        ip = hosts.objects.get(pk=ip)
        metric = Items.objects.get(pk=metric)
        print(ip, metric)
        if str(metric) == "cpu_usage":
            metricname = "CPU"
        else:
            metricname = "Memory"
        print(metricname)
        # print(ip, metric)
        sql = "SELECT clock, value FROM devsapp_history_uint where itemid_id='"+str(metric)+"' and endpoint='"+str(ip)+"' order by clock DESC LIMIT 30 "
        print(sql)
        connect = sqlite3.connect("D:/py-source/devs/db.sqlite3")
        # connect=MySQLdb.connect(host="192.168.182.179",user="root",passwd="",db="zabbix",port=3306)
        cursor = connect.cursor()
        cursor.execute(sql
            )
        datas2 = cursor.fetchall()
        for i in datas2:
            # print(i)
            times2.append(int(i[0]))
            values2.append(int(i[1]))
        times2 = [time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(i)) for i in times2]
        # times1=[i for i in range(len(times))]
        return render(request, 'asset/data.html',
                      {"hosts":hostss, "timem": timesm, "valuem": valuesm,"time": times, "value": values, "time1": times1, "value1": values1,"time2":times2,"value2":values2,"mname":metricname,"ip":ip})
    else:
        form = query_form()

    return render(request, 'asset/data.html',
                      {"hosts":hostss, "timen": timesn, "valuen": valuesn, "timem": timesm, "valuem": valuesm,"time": times, "value": values, "time1": times1, "value1": values1,})


def get_name(request):
    print(request)
    hostid = request.GET['pk']
    print(hostid)
    host = get_object_or_404(hosts, pk=hostid)
    metrics = host.items_set.all()
    print(metrics)
    print(host)
    data = serializers.serialize('json', metrics)
    return HttpResponse(data, content_type='application/json')