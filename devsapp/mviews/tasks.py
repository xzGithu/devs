#coding:utf-8
from django.shortcuts import render
from devsapp.models import ToolsScript,TaskScripts
from django.contrib.auth.decorators import login_required
import json
from django.http import HttpResponse,JsonResponse
from django.core.paginator import Paginator,EmptyPage,PageNotAnInteger


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

def maketasks(request):
    TaskScripts = ToolsScript.objects.all()

    return render(request,'tasks/task-scripts.html',context={"taskscripts":TaskScripts})

@login_required
def savetask(request):
    if request.is_ajax():
        ruleids=request.POST.get("data")
        taskname=request.POST.get("name")
        descdata = ruleids
        ruleids = eval(ruleids)
        steps = []
        for rule in  ruleids["nodeDataArray"]:
            steps.append(rule['text'].decode('utf-8'))
        taskscripts = TaskScripts.objects.filter(taskname=str(taskname).decode())
        print taskscripts
        if taskscripts:
            return HttpResponse(json.dumps({"message": "存在重名任务"}), content_type='application/json')
        else:
            TaskScripts.objects.create(taskname=str(taskname).decode(),tasksteps=steps,describe=descdata)
            return HttpResponse(json.dumps({"message":"success"}),content_type='application/json')

@login_required
def tasklist(request):
    global query
    tasks = TaskScripts.objects.all()
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
        data = tasks.filter(**kwargs)
    else:
        data = tasks

    data_list, page_range, count, page_nums = pagination(request, data)
    context = {
        'data':data_list,
        'query':query,
        'page_range':page_range,
        'count': count,
        'page_nums':page_nums,
    }
    return render(request,'tasks/task-list.html',context)

@login_required
def update(request,taskid):
    taskdata = TaskScripts.objects.get(id=taskid)
    taskscripts = ToolsScript.objects.all()
    return render(request,'tasks/update-script.html',
                  context={"taskscripts":taskscripts,"taskdata":taskdata.describe.replace("\n",""),"taskid":taskid
                           ,"taskname":taskdata.taskname},)

@login_required
def saveupdate(request):
    if request.is_ajax():
        ruleids=request.POST.get("data")
        taskname=request.POST.get("name")
        taskid = request.POST.get("taskid")
        try:
            TaskScripts.objects.filter(id=taskid).update(taskname=taskname,describe=ruleids)
            return HttpResponse(json.dumps({"message":"success"}),content_type='application/json')
        except Exception as e:
            return HttpResponse(json.dumps({"message":e}),content_type='application/json')
@login_required
def taskdel(request,taskid):
    try:
        TaskScripts.objects.filter(id=taskid).delete()
        return JsonResponse("success", safe=False)
    except:
        return JsonResponse("false", safe=False)
