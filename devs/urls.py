"""devs URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url,include
from django.contrib import admin
import devsapp.views
from devsapp.serializers import UserViewSet,eventlog_list,user_detail
from rest_framework import routers
from devsapp.mviews.perf import *
from devsapp.mviews import perf,assets,chat,ssh,intime,tasks
from devsapp.views import get_data
router = routers.DefaultRouter()
router.register(r'users', UserViewSet)

urlpatterns = [
    url(r'eventlog/$',eventlog_list),
    url(r'eventlog/(?P<id>\d+)/$',user_detail),
    url(r'^', include(router.urls)),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^admin/', admin.site.urls),
    url(r'^lists/(?P<table>\w+)/$', assets.lists, name='lists'),
    url(r'^add/(?P<table>\w+)/$', assets.add, name='add'),
    url(r'^edit/(?P<table>\w+)/(?P<pk>\d+)/$', assets.edit, name='edit'),
    url(r'^delete/(?P<table>\w+)/(?P<pk>\d+)/$', assets.delete, name='delete'),
    url(r'^index/', devsapp.views.index, name='index'),
    url(r'login/', devsapp.views.login, name='login'),
    url(r'logout/', devsapp.views.logout, name='logout'),
    url(r'password_change/', devsapp.views.password_change, name='password_change'),
    url(r'^run_ssh_cmd/', devsapp.views.cmd_commands, name='run_ssh_cmd'),
    url(r'gethostper/', perf.gethostper, name="gethostper"),
    url(r'^echodata/', devsapp.views.echodata),
    url(r'^listing/',devsapp.views.listing,),
    url(r'^get_data/', get_data, name='get_data'),
    # url(r'^run_ans_cmd/', devsapp.views.ans_module, name='run_ans_cmd'),
    url(r'ansiblecmd/', devsapp.views.script_online, name='ansiblecmd'),
    url(r'^assadd/(?P<table>\w+)/$', assets.assetadd, name='assadd'),
    url(r'^assupd/(?P<table>\w+)/(?P<pk>\d+)/$', assets.assupd, name='assupd'),
    # url(r'^usadd/(?P<table>\w+)/$',devsapp.views.useradd,name='usadd'),
    # url(r'^usupd/(?P<table>\w+)/(?P<pk>\d+)/$', devsapp.views.userchange, name='usupd'),
    url(r'^accounts/changepwd/$', devsapp.views.changepwd, name="changepwd"),
    url(r'^accounts/register/', devsapp.views.registuser, name="regist"),
    url(r'^script/', devsapp.views.editscript, name='escript'),
    url(r'^listsc/', devsapp.views.sh, name="listsc"),
    url(r'^apps/playbook/online/$', devsapp.views.script_online),
    url(r'^shedit-(?P<sid>\d+)$', devsapp.views.show_scripts, name="sh_edit"),
    url(r'^getname/', get_name, name="getname"),
    # url(r'sh.html',devsapp.views.sh),
    url(r'scinfo-(?P<nid>\d+)/', devsapp.views.scinfo),
    url(r'scdel-(?P<nid>\d+)/', devsapp.views.shdel, name="sh_del"),
    # url(r'scdel1/', devsapp.views.delete_jigui,name="sh_del1"),
    url(r'^shell-(?P<nid>\d+)/', devsapp.views.shell, name="shell"),
    url(r'^shell/', devsapp.views.shell_sh, name="shell_sh"),
    url(r'scadd/', devsapp.views.add_scripts, name='addscripts'),
    url(r'^webssh$', devsapp.views.host_web_ssh, name='webssh'),
    url(r'^socp/(?P<userid>\w+)$', devsapp.views.echo1, name='socp'),
    url(r'^output/',intime.cmdlines,name='cmdlines'),
    url(r'^taskmake/',tasks.maketasks,name='taskmake'),
    url(r'^savetask/', tasks.savetask, name='savetask'),
    url(r'^listtask/', tasks.tasklist, name='listtask'),
    url(r'^updatetask/(?P<taskid>\d+)$', tasks.update, name='updatatask'),
    url(r'^saveupdate/$', tasks.saveupdate, name='saveupdate'),
    url(r'^taskdel/(?P<taskid>\d+)$', tasks.taskdel, name='taskdel'),
    # url(r'^filer/',include('filer.urls')),
    # url(r'^apps_models/',devsapp.views.apps_model,name="apps_model")
    # url(r'^operation/',include('operation.urls.views_urls',namespace='operation')),
]
