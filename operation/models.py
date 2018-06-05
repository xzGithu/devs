# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import AbstractUser
from operation.utils import utils
# Create your models here.
class ExtendUser(AbstractUser):
    img = models.CharField(max_length=10,default='user.jpg')
    phone = models.CharField(max_length=11,default='None',)
    # groups = models.ManyToManyField(
    #     PermissionGroup,
    #     verbose_name=_('groups'),
    #     blank=True,
    #     help_text=_(
    #         'The groups this user belongs to. A user will get all permissions '
    #         'granted to each of their groups.'
    #     ),
    #     related_name="user_set",
    #     related_query_name="user",
    # )
    def get_9531email(self):
        return self.email.split('@')[0] + '@8531.cn'

    def get_full_name(self):
        """
        Returns the first_name plus the last_name, with a space in between.
        """
        full_name = '%s' % (self.last_name,)# self.first_name)
        return full_name.strip()

    def get_group_name(self):
        """
        :return: Name of group
        """
        if self.is_superuser == 1:
            return "超级管理员"
        elif self.groups.count() == 0:
            return "无权限"
        else:
            str = ""
            groups = self.groups.all()
            for group in groups:
                str += group.name + ' '
            return str

class Group(models.Model):
    id=models.AutoField(primary_key=True)
    name=models.CharField(max_length=100,default='')
    info=models.CharField(max_length=100,default='')
class Script(models.Model):
    SCRIPT_STATUS=(
        (0,u'未完成'),
        (1,u'已完成'),
    )
    id=models.AutoField(primary_key=True)
    name=models.CharField(max_length=100,default='noName')
    info=models.CharField(max_length=100,default="noUse")
    script=models.TextField(default='')
    author = models.ForeignKey(ExtendUser, default=1, related_name='suser')
    status=models.IntegerField(default=0,choices=SCRIPT_STATUS)
    def formatScript(self):
        string=""
        kwargs={}
        for args in self.scriptargs.all():
            kwargs[args.args_name] = args.args_value
        string = string + utils.bash_writer(self.author.email,'now',**kwargs)
        string = string + utils.html2bash(self.script)
        return string

class ScriptArgs(models.Model):
    id=models.AutoField(primary_key=True)
    args_name=models.CharField(max_length=100,default='')
    args_value=models.CharField(max_length=100,default='')
    script=models.ForeignKey(Script,default=1,related_name='scriptargs')


class PlayBook(models.Model):
    PLAYBOOK_STATUS=(
        (0,u'未完成'),
        (1,u'已完成'),
    )
    SUDO_STATUS=(
        (0,u'不需要'),
        (1,u'需要')
    )
    id=models.AutoField(primary_key=True)
    name = models.CharField(max_length=100,default='noName')
    author = models.ForeignKey(ExtendUser,default=1,related_name='puser')
    info = models.CharField(max_length=100,default='noUse')
    sort = models.IntegerField(default=0)
    sudo = models.IntegerField(default=1,choices=SUDO_STATUS)
    status = models.IntegerField(default=0,choices=PLAYBOOK_STATUS)
    groups = models.ManyToManyField(Group,blank=True,related_name='playbooks',verbose_name=_('Playbook'))

class Task(models.Model):
    id = models.AutoField(primary_key=True)
    module = models.CharField(default='hostname',max_length=20)
    args = models.CharField(default='',max_length=100)
    sort = models.IntegerField(default=0)
    playbook = models.ForeignKey(PlayBook,default=1,related_name='tasks')

STATUS = (
    (0, u'正在运行'),
    (1, u'运行成功'),
    (2, u'运行失败'),
)
HISTORY_TYPE = (
    (0, u'资产管理'),
    (1, u'脚本修改'),
    (2, u'剧本修改'),
    (3, u'人员管理'),
    (4, u'应用管理'),
)
class Storage(models.Model):
    id=models.AutoField(primary_key=True)#全局ID
    disk_size=models.CharField(max_length=100,default="")
    disk_path=models.CharField(max_length=100,default="")
    info=models.CharField(max_length=100,default="")

    def get_all_group_name(self):
        list = []
        for host in self.hosts.all():
            for group in host.groups.all():
                list.append(group.name)
        result={}.fromkeys(list).keys()
        str = ""
        for r in result:
            str = str + r +','
        return str[0:-1]
class Softlib(models.Model):
    SOFT_CHOICES=(
        (0,u'no'),
        (1,u'Tomcat应用'),
        (2,u'数据库'),
        (3,u'redis缓存'),
        (4,u'nginx应用'),
        (5,u'rabbitmq队列'),
    )
    id=models.AutoField(primary_key=True)
    soft_type = models.IntegerField(choices=SOFT_CHOICES,default=0)
    soft_version=models.CharField(max_length=10)
    # soft_md5=models.CharField(max_length=100,)
class Host(models.Model):
    SYSTEM_CHOICES=(
        (0,u'未添加'),
        (1,u'Windows Server 2006'),
        (2,u'Windows Server 2008'),
        (3,u'Centos 6.5'),
        (4,u'Centos 7.1'),
    )
    SYSTEM_STATUS=(
        (0,'错误'),
        (1,'正常'),
        (2,'不可达'),
    )
    id=models.AutoField(primary_key=True) #全局ID
    groups = models.ManyToManyField(Group,blank=True,related_name='hosts',verbose_name=_("Group"))#所属应用
    storages = models.ManyToManyField(Storage,blank=True,related_name='hosts',verbose_name=_('Host'))
    systemtype=models.IntegerField(default=0,choices=SYSTEM_CHOICES)#操作系统
    manage_ip = models.CharField(max_length=15, default='')#管理IP
    service_ip = models.CharField(max_length=15, default='')#服务IP
    outer_ip = models.CharField(max_length=15, default='')#外网IP
    server_position = models.CharField(max_length=50,default='')#服务器位置
    hostname = models.CharField(max_length=50,default='localhost.localdomain')#主机名称
    normal_user = models.CharField(max_length=15, default='')#普通用户
    sshpasswd = models.CharField(max_length=100,default='')#用户密码
    sshport = models.CharField(max_length=5,default='')#用户端口
    coreness = models.CharField(max_length=5,default='')#CPU数
    memory = models.CharField(max_length=7,default='')#内存
    root_disk = models.CharField(max_length=7,default="")#本地磁盘大小
    info = models.CharField(max_length=200,default="")
    status = models.IntegerField(default=1,choices=SYSTEM_STATUS)#服务器状态

    def application_get(self):
        id_list=[]
        for attr in list:
            if getattr(self,attr).count() == 0:
                pass
            else:
                id_list.append(int(getattr(self,attr).get().softlib_id))
        if Softlib.objects.filter(id__in=id_list).count() == 0:
            softlibs = []
        else:
            softlibs = Softlib.objects.filter(id__in=id_list)
        return softlibs
class History(models.Model):
    id = models.AutoField(primary_key=True)
    hosts = models.ManyToManyField(Host,blank=True,related_name='hosts',verbose_name=_("Host"))
    user = models.ForeignKey(ExtendUser, default=1, related_name='startuser') #发起用户
    type = models.IntegerField(default=0,choices=HISTORY_TYPE)#历史类型
    info = models.TextField(default='')#信息
    status = models.IntegerField(default=0,choices=STATUS)#状态
    starttime = models.DateTimeField(auto_now_add=True,blank=True)#历史开始时间
    endtime = models.DateTimeField(auto_now=True,blank=True)#历史结束时间