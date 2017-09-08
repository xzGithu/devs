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
from django.conf.urls import url
from django.contrib import admin
import devsapp.views
urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^lists/(?P<table>\w+)/$',devsapp.views.lists,name='lists'),
    url(r'^add/(?P<table>\w+)/$',devsapp.views.add,name='add'),
    url(r'^edit/(?P<table>\w+)/(?P<pk>\d+)/$', devsapp.views.edit, name='edit'),
    url(r'^delete/(?P<table>\w+)/(?P<pk>\d+)/$', devsapp.views.delete, name='delete'),
    url(r'^index/',devsapp.views.index,name='index'),
    url(r'login/', devsapp.views.login, name='login'),
    url(r'logout/', devsapp.views.logout, name='logout'),
    url(r'password_change/', devsapp.views.password_change, name='password_change'),
    url(r'^run_ssh_cmd/', devsapp.views.cmd_commands, name='run_ssh_cmd'),
    url(r'^run_ans_cmd/', devsapp.views.ans_module, name='run_ans_cmd'),
    url(r'^assadd/(?P<table>\w+)/$', devsapp.views.assetadd, name='assadd'),
    url(r'^assupd/(?P<table>\w+)/(?P<pk>\d+)/$', devsapp.views.assupd, name='assupd'),
    # url(r'^usadd/(?P<table>\w+)/$',devsapp.views.useradd,name='usadd'),
    # url(r'^usupd/(?P<table>\w+)/(?P<pk>\d+)/$', devsapp.views.userchange, name='usupd'),
    url(r'^accounts/changepwd/$', devsapp.views.changepwd, name="changepwd"),
    url(r'^accounts/register/', devsapp.views.registuser, name="regist"),
    # url(r'run/',devsapp.views.runmodule,name='run'),
]
