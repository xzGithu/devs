#coding:utf-8
from devsapp.models import Assets,SSHInfo,ToolsScript
from django.contrib.auth.models import User
from django.shortcuts import render,redirect
from django.http import JsonResponse
from django.db import IntegrityError
from django.core.paginator import EmptyPage,PageNotAnInteger,Paginator
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from devsapp.forms import HostfForm,UserForm,AssetForm
# from devsapp.api_v2 import ANSRunner

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

def lists(request,table):
    global raw_data
    global list_template,sub_title,query,page_title
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

#修改数据,函数中的pk代表数据的id
@login_required
def edit(request, table, pk):
    global form,sub_title
        #这是Django的一个快捷方法,通过pk去line表中取值，如果有值则返回，如果无值则抛出http404的异常
        #具体信息可参考https://docs.djangoproject.com/en/1.9/topics/http/shortcuts/
        #通过instance来将Form的数据做填充

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
def add(request,table):
    global form,sub_title
    page_title = '资产管理'
    #根据提交的请求不同，获取来自不同Form的表单数据
    if table == 'host':
        form = HostfForm(request.POST or None)
        sub_title = '添加主机'
    if table == 'user':
        form = UserForm(request.POST or None)
        sub_title = '添加用户'
    if form.is_valid():
        instance = form.save(commit=False)
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