# -*- coding:utf-8 -*-
from django.shortcuts import render,redirect,get_object_or_404
from .models import *
from django.db import IntegrityError
from django.http import JsonResponse,HttpResponse,HttpResponseRedirect
from django.core.paginator import Paginator,EmptyPage,PageNotAnInteger
from django.contrib.auth import views,authenticate
from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response
import paramiko
from rest_framework.serializers import ModelSerializer
# from django.views.generic.edit import FormView
# from api_v2 import ANSRunner
import json,uuid
from .forms import *
from django.contrib.auth.models import User,Group
import MySQLdb
from dwebsocket.decorators import accept_websocket,require_websocket
# from devsapp.ansible_runner.runner import AdHocRunner,PlayBookRunner
# from devsapp.ansible_runner.callback import CommandResultCallback

#分页函数
def pagination(request, queryset, display_amount=10, after_range_num = 5,before_range_num = 4):
    #按参数分页
    try:
        #从提交来的页面获得page的值
        page = int(request.GET.get("page", 1))
        #如果page值小于1，那么默认为第一页
        if page < 1:
            page = 1
    #若报异常，则page为第一页
    except ValueError:
            page = 1
    #引用Paginator类
    paginator = Paginator(queryset, display_amount)
    #总计的数据条目
    count = paginator.count
    #合计页数
    num_pages = paginator.num_pages

    try:
        #尝试获得分页列表
        objects = paginator.page(page)
    #如果页数不存在
    except EmptyPage:
        #获得最后一页
        objects = paginator.page(paginator.num_pages)
    #如果不是一个整数
    except PageNotAnInteger:
        #获得第一页
        objects = paginator.page(1)
    #根据参数配置导航显示范围
    temp_range = paginator.page_range

    #如果页面很小
    if (page - before_range_num) <= 0:
        #如果总页面比after_range_num大，那么显示到after_range_num
        if temp_range[-1] > after_range_num:
            page_range = xrange(1, after_range_num+1)
        #否则显示当前页
        else:
            page_range = xrange(1, temp_range[-1]+1)
    #如果页面比较大
    elif (page + after_range_num) > temp_range[-1]:
        #显示到最大页
        page_range = xrange(page-before_range_num,temp_range[-1]+1)
    #否则在before_range_num和after_range_num之间显示
    else:
        page_range = xrange(page-before_range_num+1, page+after_range_num)
    #返回分页相关参数
    return objects, page_range, count, num_pages

##列表函数
@login_required
def lists(request,table):
    global raw_data
    global list_template,sub_title,query,page_title


    # data = Node.objects.all()
    # list_template = 'node_list.html'
    if table == 'node':
        raw_data = Node.objects.order_by('id')
        list_template = 'node_list.html'
        sub_title = '机房信息'
        page_title = '基础信息'
    if table == 'line':
        raw_data = Line.objects.order_by('id')
        list_template = 'line_list.html'
        sub_title = '线路信息'
        page_title = '基础信息'
    if table == 'device':
        # raw_data = Device.objects.all()
        raw_data = Device.objects.order_by('id')
        list_template = 'device_list.html'
        sub_title = '设备信息'
        page_title = '基础信息'
    if table == 'host':
        raw_data = SSHInfo.objects.order_by('id')
        list_template = 'ssh/host_list.html'
        sub_title = '主机列表'
        page_title = 'SSH'
    if table == 'asset':
        raw_data = Assets.objects.order_by('id')
        list_template = 'asset/ass_list.html'
        sub_title = '资产列表'
        page_title = '资产管理'
    if table == 'user':
        raw_data = User.objects.order_by('id')
        list_template = 'user/user_list.html'
        sub_title = '用户列表'
        page_title = '用户管理'
    if request.method == 'GET':
        kwargs = {}
        query = ''
        for key, value in request.GET.iteritems():
            if key != 'csrfmiddlewaretoken' and key != 'page':
                if key == 'node':
                    kwargs['node__node_name__contains'] = value
                    query += '&' + key + '=' + value
                else:
                    kwargs[key + '__contains'] = value
                    query += '&' + key + '=' + value
        data = raw_data.filter(**kwargs)
    else:
        data = raw_data

    data_list, page_range, count, page_nums = pagination(request, data)
    context = {
        'data':data_list,
        'table':table,
        'query':query,
        'page_range':page_range,
        'count': count,
        'page_nums':page_nums,
        'page_title':page_title,
        'sub_title':sub_title
    }
    return render(request,list_template,context)

@login_required
def add(request,table):
    global form,sub_title
    page_title = '资产管理'
    #根据提交的请求不同，获取来自不同Form的表单数据
    if table == 'node':
        form = NodeForm(request.POST or None)
        sub_title = '添加机房'
    if table == 'line':
        form = LineForm(request.POST or None)
        sub_title = '添加线路'
    if table == 'device':
        form = DeviceForm(request.POST or None)
        sub_title = '添加设备'
    if table == 'host':
        form = HostfForm(request.POST or None)
        sub_title = '添加主机'
    if table == 'user':
        form = UserForm(request.POST or None)
        sub_title = '添加用户'
    if form.is_valid():
        instance = form.save(commit=False)
        if table == 'node':
            instance.node_signer = request.user
        if table == 'line':
            instance.line_signer = request.user
        if table == 'device':
            instance.device_signer = request.user
        if table == 'host':
            instance.state = 1
        if table == 'user':
            instance.is_active = True

        instance.save()
        return redirect('lists',table = table)
    context = {
        'form':form,
        'table':table,
        'page_title':page_title,
        'sub_title':sub_title,
    }
    return render(request,'res_add.html',context)

@login_required
def assetadd(request,table):
    global form,sub_title
    page_title = '资产管理'
    if table == 'asset':
        form = AssetForm(request.POST or None)
        sub_title = '添加资产'
    if form.is_valid():
        instance = form.save(commit=False)
        if table == 'asset':
            instance.status = 1

        instance.save()
        return redirect('lists',table = table)
    context = {
        'form':form,
        'table':table,
        'page_title':page_title,
        'sub_title':sub_title,
    }
    return render(request,'asset/resass_add.html',context)

@login_required
def assupd(request,table,pk):
    global table_ins
    if table == 'asset':
        # ip = Assets.objects.filter(pk=pk)
        table_ins = get_object_or_404(Assets, pk=pk)

    if request.method == 'POST':
        # ip = Assets.objects.filter(pk=pk)
        try:
            resource = []
            dict = {}


            dict['hostname'] = table_ins.ip
            dict["username"] = SSHInfo.objects.filter(host=table_ins.ip)[0].usr
            dict["password"] = SSHInfo.objects.filter(host=table_ins.ip)[0].pwd

            resource.append(dict)
            print resource
            abt = ANSRunner(resource)
            hostlist=[]
            hostlist.append(table_ins.ip)
            abt.run_model(host_list=hostlist, module_name="setup", module_args=" ")
            data = abt.get_setmodel_result()
            result = abt.handle_cmdb_data(data)[0]

            Assets.objects.filter(ip=table_ins.ip).update(**result)
            if result["status"]==1:
                mess = 'error'
            else:
                mess = 'success'
        except:
            mess = 'error'


        return JsonResponse(mess,safe=False)
#显示首页
@login_required
def index(request):
    #获取相应信息
    node_number = Node.objects.count()
    line_number = Line.objects.count()
    device_number = Device.objects.count()
    host_number = Assets.objects.count()

    # task_number = Task.objects.count()
    # #获取已结单的数量,用于计算任务完成率
    # task_complete = Task.objects.filter(task_status='已结单').count()
    # #用float可以保留小树，round保留小数点2位
    # task_complete_percent = round(float(task_complete)/task_number*100,2)
    #将相关参数传递给dashboard页面
    context = {
        'node_number': node_number,
        'line_number': line_number,
        'device_number': device_number,
        'host_number': host_number,
        'page_title':"汇总信息",
        'sub_title':"一览",
        # 'task_number': task_number,
        # 'task_complete': task_complete,
        # 'task_complete_percent': task_complete_percent,
    }
    return render(request,'dashboard.html',context)


#修改数据,函数中的pk代表数据的id
@login_required
def edit(request, table, pk):
    global form,sub_title
    if table == 'line':
        #这是Django的一个快捷方法,通过pk去line表中取值，如果有值则返回，如果无值则抛出http404的异常
        #具体信息可参考https://docs.djangoproject.com/en/1.9/topics/http/shortcuts/
        table_ins = get_object_or_404(Line, pk=pk)
        #通过instance来将Form的数据做填充
        form = LineForm(request.POST or None, instance=table_ins)
        sub_title = '修改线路信息'
    if table == 'node':
        table_ins = get_object_or_404(Node, pk=pk)
        form = NodeForm(request.POST or None, instance=table_ins)
        sub_title = '修改机构信息'
    if table == 'device':
        table_ins = get_object_or_404(Device, pk=pk)
        form = DeviceForm(request.POST or None, instance=table_ins)
        sub_title = '修改设备信息'
    if table == 'host':
        table_ins = get_object_or_404(SSHInfo,pk=pk)
        form = HostfForm(request.POST or None,instance=table_ins)
        sub_title = '修改主机信息'
    if table == 'user':
        table_ins = get_object_or_404(User,pk=pk)
        form = UserForm(request.POST or None,instance=table_ins)
        sub_title = '修改用户信息'
    #判断form是否有效
    if form.is_valid():
        #创建实例，需要做些数据处理，暂不做保存
        instance = form.save(commit=False)
        #将登录用户作为登记人,在修改时，一定要使用str强制,因为数据库中以charfield方式存放了登记人
        if table == 'node':
            instance.node_signer = str(request.user)
        if table == 'line':
            instance.line_signer = str(request.user)
        if table == 'device':
            instance.device_signer = str(request.user)
        if table == 'host':
            instance.state = 1
        if table == 'user':
            instance.is_active = True
        #保存该实例
        instance.save()
        #跳转至列表页面,配合table参数，进行URL的反向解析
        return redirect('lists', table=table)

    context = {
        'table': table,
        'form': form,
        'sub_title': sub_title,
    }
    #与res_add.html用同一个页面，只是edit会在res_add页面做数据填充
    return render(request, 'res_add.html', context)

@login_required
def delete(request, table ,pk):
    global table_ins
    #选择相应的表格
    if table == 'line':
        #通过id值获取相应表格的实例，有值则返回，无值则抛出异常
        table_ins = get_object_or_404(Line, pk=pk)

    if table == 'node':
        table_ins = get_object_or_404(Node, pk=pk)

    if table == 'device':
        table_ins = get_object_or_404(Device, pk=pk)
    if table == 'host':
        table_ins = get_object_or_404(SSHInfo,pk=pk)

    if table == 'user':
        table_ins = get_object_or_404(User,pk=pk)
    if table == 'toolscripts':
        table_ins = get_object_or_404(ToolsScript,pk=pk)

    #接收通过AJAX提交过来的POST
    if request.method == 'POST':
        #删除该条目
        try:
            table_ins.delete()
            #删除成功,则data信息为success
            data = 'success'
        except IntegrityError:
            #如因外键问题，或其他问题，删除失败，则报error
            data = 'error'
        #将最后的data值传递至JS页面，进行后续处理
        return JsonResponse(data,safe=False)


@login_required
def script_online(request):
    global fileName,playbook_server_value
    if request.method == "GET":
        serverList = Server_Assets.objects.all()
        # groupList = Group.objects.all()
        userList = User.objects.all()
        serviceList = service_assets.objects.all()
        return render(request,'file/apps_playbook_online.html',{"user":request.user,"userList":userList,
                                                            "serverList":serverList,"serviceList":serviceList},
                                  )
    elif request.method == "POST":
        sList = []
        if request.POST.get('server_model') in ['service','custom']:
            if request.POST.get('server_model') == 'custom':
                for sid in request.POST.getlist('playbook_server[]'):
                    server = Server_Assets.objects.get(id=sid)
                    sList.append(server.ip)
                playbook_server_value = None
            elif request.POST.get('server_model') == 'service':
                serverList = Assets.objects.filter(business=request.POST.get('ansible_service'))
                sList = [  s.server_assets.ip for s in serverList ]
                playbook_server_value = request.POST.get('ansible_service')
            fileName = '/upload/playbook/online-{ram}.yaml'.format(ram=uuid.uuid4().hex[0:8])
            filePath = os.getcwd() + fileName
            if request.POST.get('playbook_content'):
                with open(filePath, 'w') as f:
                    f.write(request.POST.get('playbook_content'))
            else:
                return JsonResponse({'msg':"文件内容不能为空","code":500,'data':[]})
        try:
            playbook = Ansible_Playbook.objects.create(
                                            playbook_name = request.POST.get('playbook_name'),
                                            playbook_desc = request.POST.get('playbook_desc'),
                                            playbook_vars = request.POST.get('playbook_vars'),
                                            playbook_uuid = uuid.uuid4(),
                                            playbook_file = fileName,
                                            playbook_server_model = request.POST.get('server_model','custom'),
                                            playbook_server_value = playbook_server_value,
                                            playbook_auth_group = request.POST.get('playbook_auth_group',0),
                                            playbook_auth_user = request.POST.get('playbook_auth_user',0),
                                            playbook_type = 1
                                            )
        except Exception, ex:
            return JsonResponse({'msg':str(ex),"code":500,'data':[]})
        for sip in sList:
            try:
                Ansible_Playbook_Number.objects.create(playbook=playbook,playbook_server=sip)
            except Exception, ex:
                playbook.delete()
                print ex
        #操作日志异步记录
        # AnsibleRecord.PlayBook.insert(user=str(request.user),ans_id=playbook.id,ans_name=playbook.playbook_name,ans_content="添加Ansible剧本",ans_server=','.join(sList))
        return JsonResponse({'msg':None,"code":200,'data':[]})

def add_scripts(request):
    if request.method == "POST":
        name = request.POST.get('name', None)
        tool_script = request.POST.get('tool_script', None)
        tool_run_type = request.POST.get('tool_run_type', None)
        comment = request.POST.get('comment', None)
        obj = ToolsScript.objects.create(name=name,tool_script=tool_script,tool_run_type=tool_run_type,comment=comment)
        msg = "添加成功"
        context = {"page_title": 'SCRIPTS', "sub_title": 'ADD',"msg":msg }
        return render(request, 'scripts/sc_add.html', context=context)
    else:
        context = {"page_title": 'SCRIPTS', "sub_title": 'ADD', }
        return render(request, 'scripts/sc_add.html',context=context)
    # context = { "page_title": 'SCRIPTS', "sub_title": 'ADD',}
    # return render(request,'scripts/sc_add.html',context=context)

def show_scripts(request,sid):
    if request.method == "GET":
        obj1 = ToolsScript.objects.filter(id=sid)
        return render(request, 'scripts/shedit.html', {'obj': obj1,"page_title": '脚本编辑',"sub_title":obj1[0].name})

    elif request.method == "POST":
        name = request.POST.get('name', None)
        tool_script = request.POST.get('tool_script', None)
        tool_run_type = request.POST.get('tool_run_type', None)
        comment = request.POST.get('comment', None)
        obj1 = ToolsScript.objects.filter(id=sid).first()
        obj1.name = name
        obj1.tool_script = tool_script
        obj1.tool_run_type = tool_run_type
        obj1.comment = comment
        obj1.save()
        return redirect('/listsc')

def shdel(request,nid):  # 删除
    # ret = {'status': 'success', 'data': 'success'}
    # print ret
    if request.method == "POST":
        try:
            obj1 = ToolsScript.objects.filter(id=nid).delete()
            data = 'success'
        except:
            data = 'error'
        return JsonResponse(data,safe=False)


def shell(request, nid):  ##执行脚本页面
    # print nid
    if request.method == "GET":
        obj = Assets.objects.filter(id__gt=0)
        print obj
        sh = ToolsScript.objects.filter(id=nid)

        return render(request, 'scripts/shell.html', {"host_list": obj, "sh": sh})
def shell_sh(request):  ##执行脚本-执行
    ret = {'status': True, 'data': None}
    if request.method == 'POST':
        try:
            host_ids = request.POST.getlist('id', None)
            sh_id = request.POST.get('shid', None)
            # print host_ids
            user = request.user
            if not host_ids:
                error1 = "请选择主机"
                ret = {"error": error1, "status": False}
                return HttpResponse(json.dumps(ret))

            idstring = ','.join(host_ids)
            # print idstring

            host = SSHInfo.objects.extra(where=['id IN (' + idstring + ')'])
            host1 = SSHInfo.objects.filter(id=host_ids)
            sh = ToolsScript.objects.filter(id=sh_id)
            print sh
            print host

            for s in sh:
                if s.tool_run_type == 0:
                    with  open('scripts/shell/test.sh', 'w+') as f:
                        f.write(s.tool_script)
                        a = 'scripts/shell/{}.sh'.format(s.id)
                    os.system("sed 's/\r//'  scripts/shell/test.sh >  {}".format(a))

                elif s.tool_run_type == 1:
                    with  open('scripts/shell/test.py', 'w+') as f:
                        f.write(s.tool_script)
                        p = 'scripts/shell/{}.py'.format(s.id)
                    os.system("sed 's/\r//'  scripts/shell/test.py >  {}".format(p))
                elif s.tool_run_type == 2:
                    with  open('scripts/shell/test.yml', 'w+') as f:
                        f.write(s.tool_script)
                        y = 'scripts/shell/{}.yml'.format(s.id)
                    os.system("sed 's/\r//'  scripts/shell/test.yml >  {}".format(y))
                else:
                    ret['status'] = False
                    ret['error'] = '脚本类型错误,只能是shell、yml、python'
                    return HttpResponse(json.dumps(ret))

                data1 = []
                for h in host:
                    try:
                        data2 = {}
                        assets = [
                            {
                                "hostname": h.hostname,
                                "ip": h.ip,
                                "port": h.port,
                                "username": h.username,
                                "password": h.password,
                            },
                        ]

                        # history = History.objects.create(ip=h.ip, root=h.username, port=h.port, cmd=s.name, user=user)
                        if s.tool_run_type == 0:
                            task_tuple = (('script', a),)
                            hoc = AdHocRunner(hosts=assets)
                            hoc.results_callback = CommandResultCallback()
                            r = hoc.run(task_tuple)
                            data2['ip'] = h.ip
                            data2['data'] = r['contacted'][h.hostname]['stdout']
                            data1.append(data2)
                        elif s.tool_run_type == 1:
                            task_tuple = (('script', p),)
                            hoc = AdHocRunner(hosts=assets)
                            hoc.results_callback = CommandResultCallback()
                            r = hoc.run(task_tuple)
                            data2['ip'] = h.ip
                            data2['data'] = r['contacted'][h.hostname]['stdout']
                            data1.append(data2)
                        elif s.tool_run_type == 2:
                            play = PlayBookRunner(assets, playbook_path=y)
                            b = play.run()
                            print(b)
                            data2['ip'] = h.ip
                            data2['data'] = b['plays'][0]['tasks'][1]['hosts'][h.hostname]['stdout'] + \
                                            b['plays'][0]['tasks'][1]['hosts'][h.hostname]['stderr']
                            print(data2['data'])

                            print(data2)
                            data1.append(data2)
                        else:
                            data2['ip'] = "脚本类型错误"
                            data2['data'] = "脚本类型错误"
                    except  Exception as  e:
                        data2['ip'] = h.ip
                        data2['data'] = "账号密码不对，请修改 {}".format(e)
                        data1.append(data2)

                ret['data'] = data1
                print(ret)
                return HttpResponse(json.dumps(ret))
        except Exception as e:
            ret['status'] = False
            ret['error'] = '未知错误 {}'.format(e)
            return HttpResponse(json.dumps(ret))


def scinfo(request, nid):  # 查看
    if request.method == "GET":
        obj1 = ToolsScript.objects.filter(id=nid)
        return render(request, 'scripts/shinfo.html', {'obj': obj1})

def sh(request):  ##首页
    sh = ToolsScript.objects.filter(id__gt=0).order_by('-id')
    return render(request, 'scripts/sh.html', {"sh_list": sh, })

#用户登陆选项，所有的函数将会返回一个template_response的实例，用来描绘页面，同时你也可以在return之前增加一些特定的功能
#用户登陆
def login(request):
    #extra_context是一个字典，它将作为context传递给template，这里告诉template成功后跳转的页面将是/index
    template_response = views.login(request, extra_context={'next': '/index'})
    return template_response

#用户退出
def logout(request):
    #logout_then_login表示退出即跳转至登陆页面，login_url为登陆页面的url地址
    template_response = views.logout_then_login(request,login_url='/login')
    return template_response

#密码更改
def password_change(request):
    #post_change_redirect表示密码成功修改后将跳转的页面.
    template_response = views.password_change(request,post_change_redirect='/index')
    return template_response

#

def registuser(request):
    if request.method == 'POST':
        form = RegistForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            repassword = form.cleaned_data['repassword']
            email = form.cleaned_data['email']

            if password==repassword:
                exuser = User.objects.filter(username = username)
                if len(exuser) > 0:
                    err = '用户名已存在'
                    return render(request, 'user/useradd.html', {'form': form,'error':err,'page_title':"用户管理",'sub_title':"用户",})
            else:
                err='密码不匹配'
                return render(request, 'user/useradd.html',{'form': form, 'error': err, 'page_title': "用户管理", 'sub_title': "用户", })

            user = User.objects.create_user(username=username,password=password,email=email)
            user.save()

            return HttpResponseRedirect('/lists/user',)
    else:
        form = RegistForm()
    return render(request,'user/useradd.html',{'form':form,'page_title':"用户管理",'sub_title':"用户",})

def changepwd(request):
    if request.method == 'GET':
        form = ChangepwdForm()
        return render(request,'user/changepwd.html', {'form': form, 'page_title':"用户管理",'sub_title':"用户",})
    else:
        form = ChangepwdForm(request.POST)
        if form.is_valid():
            username = request.user.username
            oldpassword = request.POST.get('oldpassword', '')
            user = authenticate(username=username, password=oldpassword)
            if user is not None and user.is_active:
                newpassword = request.POST.get('newpassword1', '')
                user.set_password(newpassword)
                user.save()
                return render(request,'user/afterchangepwd.html',  {'changepwd_success': True,'page_title':"用户管理",'sub_title':"用户", })
            else:
                return render(request,'user/changepwd.html',  {'form': form, 'oldpassword_is_wrong': True, 'page_title':"用户管理",'sub_title':"用户",})
        else:
            return render(request,'user/changepwd.html', {'form': form, 'page_title':"用户管理",'sub_title':"用户", })

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


def editscript(request):
    if request.method == 'POST':
        form = ScriptCreateUpdateForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            script = form.cleaned_data['script']
            info = form.cleaned_data['info']
            path = 'D:/'
            f = open(os.path.join(path,name),'w')
            f.write(script)
            f.close()
            form.save()
            return redirect('listsc')
            # return render(request,'file/script.html',)
    else:
        form = ScriptCreateUpdateForm()
    return render(request,'file/script.html',{"form":form})

def listsc(request):
    global query
    listssc=ToolsScript.objects.order_by('id')
    if request.method == 'GET':
        kwargs = {}
        query = ''
        for key, value in request.GET.iteritems():
            if key != 'csrfmiddlewaretoken' and key != 'page':
                if key == 'node':
                    kwargs['node__node_name__contains'] = value
                    query += '&' + key + '=' + value
                else:
                    kwargs[key + '__contains'] = value
                    query += '&' + key + '=' + value
        data = listssc.filter(**kwargs)
    else:
        data = listssc

    data_list, page_range, count, page_nums = pagination(request, data)
    context = {
        'data':data_list,
        # 'table':table,
        'query':query,
        'page_range':page_range,
        'count': count,
        'page_nums':page_nums,
        'page_title':"SCRIPTS",
        'sub_title':"lists"
    }
    return render(request,'file/sclist.html',context)

def host_web_ssh(request):   ##  web ssh 登陆
    if request.method == 'POST':
        id = request.POST.get('id', None)
        obj = SSHInfo.objects.filter(id=id).first()
        ip = obj.ip+":"+obj.port
        username = obj.username
        password = obj.password
        ret = {"ip":ip,"username":username,'password':password,"static":True}
        return HttpResponse(json.dumps(ret))


# def commandapi(request):
#     if request.method == "POST":
@login_required
def gethostper(request):
    connect=MySQLdb.connect(host="192.168.182.179",user="root",passwd="",db="zabbix",port=3306)
    cursor=connect.cursor()
    cursor.execute("select clock,value from history_uint where itemid=28564 limit 100")
    datas=cursor.fetchall()
    times=[]
    values=[]
    for i in datas:
        times.append(int(i[0]))
        values.append(int(i[1]))
    return render(request,'asset/data.html',{"time":times,"value":values})

def echodata(request,data):
    return HttpResponse(data)

from collections import  defaultdict
allconn=defaultdict(list)

@login_required
@accept_websocket
def echo1(request,userid):
    allresult = {}
    # 获取用户信息
    userinfo = request.user
    allresult['userinfo'] = userinfo
    # 声明全局变量
    global allconn
    if not request.is_websocket():  # 判断是不是websocket连接
        try:  # 如果是普通的http方法
            message = request.GET['message']
            return HttpResponse(message)
        except:
            return render(request, 'chat.html', allresult)
    else:
        # 将链接(请求？)存入全局字典中
        allconn[str(userid)] = request.websocket
        # 遍历请求地址中的消息
        for message in request.websocket:
            # 将信息发至自己的聊天框
            request.websocket.send(message)
            # 将信息发至其他所有用户的聊天框
            for i in allconn:
                if i != str(userid):
                    allconn[i].send(message)
def anot(request):
    global a
    pass