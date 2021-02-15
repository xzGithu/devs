#coding:utf-8
from dwebsocket.decorators import accept_websocket,require_websocket
from django.http import HttpResponse
from django.shortcuts import render
import paramiko
import json


@accept_websocket
def cmdlines(request):
    if not request.is_websocket():
        try:
            message = request.GET('message')
            return HttpResponse(message)
        except:
            return render(request,'apps/cmdlines.html')
    else:
        for message in request.websocket:
            message = eval(message.decode('utf-8'))
            hostname = message["hostname"]
            username = message["username"]
            command = message["mingling"]
            password = '1qaz@WSX'
            # command = request.POST.get('command')
            ssh = paramiko.SSHClient()
            ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            # request.websocket.send('[Errno None] Unable to connect to port 22 on 127.0.0.1')
            # errcode = ''
            try:
                ssh.connect(hostname=hostname, username=username, password=password)
            except Exception as e:
                # errcode = e
                # return render(request, 'apps/cmdlines.html', {"errcode":errcode})
                request.websocket.send(e)

            # # 务必要加上get_pty=True,否则执行命令会没有权限
            stdin, stdout, stderr = ssh.exec_command(command, get_pty=True)
            # result = stdout.read()
            # 循环发送消息给前端页面
            while True:
                nextline = stdout.readline().strip()  # 读取脚本输出内容
                print nextline
                # print(nextline.strip())

                request.websocket.send(nextline.encode('utf-8'))  # 发送消息到客户端
                # 判断消息为空时,退出循环
                if not nextline:
                    break

            ssh.close()  # 关闭ssh连接
        # else:
        #     request.websocket.send('小样儿，没权限!!!'.encode('utf-8'))