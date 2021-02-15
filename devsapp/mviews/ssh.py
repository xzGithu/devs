#coding:utf-8
from devsapp.models import ToolsScript
from devsapp.forms import PlayHost
import paramiko
from django.shortcuts import render

def sh(request):  ##首页
    sh = ToolsScript.objects.filter(id__gt=0).order_by('-id')
    return render(request, 'scripts/sh.html', {"sh_list": sh, })

def cmd_commands(request):
    context = {}
    result = ''
    if request.method == 'POST':
        form = PlayHost(request.POST)
        if form.is_valid():
            ip = form.cleaned_data['ips']
            usr = form.cleaned_data['user']
            pwd = form.cleaned_data['pwd']
            comm = str(form.cleaned_data['comm'])
            ssh = paramiko.SSHClient()
            ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            ssh.connect(hostname=str(ip),username=str(usr),password=str(pwd))
            stdin,stdout,stderr = ssh.exec_command(comm)
            result = stdout.read()
            # context['result'] = stdout.read()
        # return render(request,'ssh/sshlist.html',context)
    else:
        form = PlayHost()
    context = {"form":form,"page_title":'SSH',"sub_title":'command',"result":result}
    return render(request,'ssh/sshlist.html',context)