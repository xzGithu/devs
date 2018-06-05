# -*-coding:utf-8 -*-
from __future__ import unicode_literals
from devsapp import utils
from django.db import models
# import os
# from django.contrib.auth.models import User, Group, Permission
# from django.utils.translation import ugettext as _
# Create your models here.

TOOL_RUN_TYPE = (
    (0, 'shell'),
    (1, 'python'),
    (2, 'yml'),
)
class ToolsScript(models.Model):
    name = models.CharField(max_length=255, verbose_name='工具名称')
    tool_script = models.TextField(verbose_name='脚本')
    # tools_type = models.ForeignKey(ToolsTypes, verbose_name='工具类型')
    # tool_run_type = models.CharField(max_length=255, verbose_name='脚本类型')
    tool_run_type = models.IntegerField(choices=TOOL_RUN_TYPE, verbose_name='脚本类型', default=0)
    comment = models.TextField(verbose_name='工具说明', null=True, blank=True)
    ctime = models.DateTimeField(auto_now_add=True, null=True, verbose_name='创建时间')
    utime = models.DateTimeField(auto_now=True, null=True, verbose_name='更新时间')

    def __str__(self):
        return self.name

    class Meta:
        db_table = "ToolsScript"
        verbose_name = "工具"
        verbose_name_plural = verbose_name


class Node(models.Model):
    type=(
        (U'北京','北京'),
        (U'其他','其他'),
    )
    node_name = models.CharField(verbose_name='机房名字',max_length=32)
    node_type = models.CharField(verbose_name='机房类型',max_length=32,choices=type)
    node_address = models.CharField(verbose_name='机房地址',max_length=62)
    node_contanct = models.CharField(verbose_name='机房联系人',max_length=32)
    node_signer = models.CharField(verbose_name='机房登记人',max_length=32)
    node_remarks = models.CharField(verbose_name='备注',max_length=64)
    node_signtime = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return self.node_name


class Line(models.Model):
    node = models.ForeignKey(Node,on_delete=models.PROTECT)
    spname = (
        (u'联通','联通'),
        (u'电信','电信'),
        (u'移动','移动'),
    )
    speed = (
        ('2M','2M'),
        ('4M','4M'),
        ('8M','8M'),
    )
    type = (
        ('MSTP','MSTP'),
        ('MSDP','MSDP')
    )

    line_code = models.CharField(verbose_name='线路编号',max_length=32)
    line_local = models.CharField(verbose_name='所在区域',max_length=64,default='北京')
    line_speed = models.CharField(verbose_name='线路速率',max_length=32,choices=speed,default='6M')
    line_spname = models.CharField(verbose_name='运营商',max_length=32,choices=spname)
    line_type = models.CharField(verbose_name='线路类型',max_length=32,choices=type)
    line_status = models.BooleanField(verbose_name='线路启用',default=True)
    line_open = models.DateField(verbose_name='开通时间')
    line_close = models.DateField(verbose_name='关闭时间',blank=True,null=True)
    line_signer = models.CharField(verbose_name='线路登记人',max_length=32)
    line_signtime = models.DateTimeField(auto_now_add=True)
    line_remarks = models.CharField(verbose_name='线路备注',max_length=255,blank=True)
    def __unicode__(self):
        return self.line_code

class Device(models.Model):
    node = models.ForeignKey(Node,on_delete=models.PROTECT)
    verdor = (
        ('huawei','huawei'),
        ('cisco','cisco'),
        ('lenovo','lenovo'),
    )

    device_caption = models.CharField(verbose_name='设备名称',max_length=64)
    device_serial = models.CharField(verbose_name='设备序列号',max_length=64)
    device_vendor = models.CharField(verbose_name='设备厂商',max_length=32,choices=verdor,default='huawei')
    device_type = models.CharField(verbose_name='设备类型',max_length=32)
    device_remarks = models.CharField(verbose_name='备注',max_length=255)
    device_ip = models.GenericIPAddressField(verbose_name='设备ip')
    device_status = models.CharField(verbose_name='设备状态',max_length=32)
    device_signer = models.CharField(verbose_name='登记人',max_length=32)
    device_signtime = models.DateTimeField(auto_now_add=True)
    device_user = models.CharField(verbose_name='设备用户名',max_length=32)
    device_password = models.CharField(verbose_name='设备密码',max_length=32)
    def __unicode__(self):
        return self.device_caption

class SSHInfo(models.Model):
    host_name = models.CharField(max_length=100)
    host = models.CharField(max_length=100)
    port = models.IntegerField(default=22)
    usr = models.CharField(max_length=50)
    pwd = models.CharField(max_length=100)
    ssh_key = models.TextField(null=True,blank=True)
    state = models.IntegerField(default=0)

    def __unicode__(self):
        return u'%s' % self.host



class Assets(models.Model):
    ip = models.CharField(max_length=32)
    hostname = models.CharField(max_length=32)
    cpu_number = models.IntegerField(null=True,blank=True,default=1)
    kernel = models.CharField(max_length=64,blank=True)
    model = models.CharField(max_length=32,blank=True)
    system = models.CharField(max_length=64,blank=True)
    vcpu_number = models.IntegerField(blank=True,null=True,default=1)
    status = models.IntegerField(blank=True,null=True)
    disk_total = models.CharField(max_length=12,blank=True)
    cpu_core = models.IntegerField(blank=True,null=True,default=2)
    swap = models.CharField(max_length=12,blank=True)
    ram_total = models.CharField(max_length=12,blank=True)
    selinux = models.CharField(max_length=12,blank=True)
    serial = models.CharField(max_length=32,blank=True)
    cpu = models.CharField(max_length=64,blank=True)
    manufacturer = models.CharField(max_length=32,blank=True)
    buiness = models.CharField(max_length=100,blank=True)
    def __unicode__(self):
        return self.ip



class Server_Assets(models.Model):
    assets = models.OneToOneField('Assets')
    ip = models.CharField(max_length=100,unique=True,blank=True,null=True)
    hostname = models.CharField(max_length=100,blank=True,null=True)
    username = models.CharField(max_length=100,blank=True,null=True)
    passwd = models.CharField(max_length=100,blank=True,null=True)
    keyfile =  models.SmallIntegerField(blank=True,null=True)#FileField(upload_to = './upload/key/',blank=True,null=True,verbose_name='密钥文件')
    port = models.DecimalField(max_digits=6,decimal_places=0,blank=True,null=True)
    line = models.CharField(max_length=100,blank=True,null=True)
    cpu = models.CharField(max_length=100,blank=True,null=True)
    cpu_number = models.SmallIntegerField(blank=True,null=True)
    vcpu_number = models.SmallIntegerField(blank=True,null=True)
    cpu_core = models.SmallIntegerField(blank=True,null=True)
    disk_total = models.CharField(max_length=100,blank=True,null=True)
    ram_total= models.CharField(max_length=100,blank=True,null=True)
    kernel = models.CharField(max_length=100,blank=True,null=True)
    selinux = models.CharField(max_length=100,blank=True,null=True)
    swap = models.CharField(max_length=100,blank=True,null=True)
    raid = models.SmallIntegerField(blank=True,null=True)
    system = models.CharField(max_length=100,blank=True,null=True)
    create_date = models.DateTimeField(auto_now_add=True)
    update_date = models.DateTimeField(auto_now_add=True)
    '''自定义添加只读权限-系统自带了add change delete三种权限'''
    class Meta:
        db_table = 'opsmanage_server_assets'
        permissions = (
            ("can_read_server_assets", "读取服务器资产权限"),
            ("can_change_server_assets", "更改服务器资产权限"),
            ("can_add_server_assets", "添加服务器资产权限"),
            ("can_delete_server_assets", "删除服务器资产权限"),
        )
        verbose_name = '服务器资产表'
        verbose_name_plural = '服务器资产表'


class service_assets(models.Model):
    service_name = models.CharField(max_length=100,unique=None)
    db_table = 'opsmanage_service_assets'
    permissions = (
        ("can_read_service_assets", "读取业务资产权限"),
        ("can_change_service_assets", "更改业务资产权限"),
        ("can_add_service_assets", "添加业务资产权限"),
        ("can_delete_service_assets", "删除业务资产权限"),
    )
    verbose_name = '业务分组表'
    verbose_name_plural = '业务分组表'


class Ansible_Playbook(models.Model):
    playbook_name = models.CharField(max_length=50,verbose_name='剧本名称',unique=True)
    playbook_desc = models.CharField(max_length=200,verbose_name='功能描述',blank=True,null=True)
    playbook_vars = models.TextField(verbose_name='模块参数',blank=True,null=True)
    playbook_uuid = models.CharField(max_length=50,verbose_name='唯一id')
    playbook_file = models.FileField(upload_to = './upload/playbook/',verbose_name='剧本路径')
    playbook_auth_group = models.SmallIntegerField(verbose_name='授权组',blank=True,null=True)
    playbook_auth_user = models.SmallIntegerField(verbose_name='授权用户',blank=True,null=True,)
    class Meta:
        db_table = 'opsmanage_ansible_playbook'
        permissions = (
            ("can_read_ansible_playbook", "读取Ansible剧本权限"),
            ("can_change_ansible_playbook", "更改Ansible剧本权限"),
            ("can_add_ansible_playbook", "添加Ansible剧本权限"),
            ("can_delete_ansible_playbook", "删除Ansible剧本权限"),
        )
        verbose_name = 'Ansible剧本配置表'
        verbose_name_plural = 'Ansible剧本配置表'


class Ansible_Playbook_Number(models.Model):
    playbook = models.ForeignKey('Ansible_Playbook', related_name='server_number', on_delete=models.CASCADE)
    playbook_server = models.CharField(max_length=100, verbose_name='目标服务器', blank=True, null=True)

    class Meta:
        db_table = 'opsmanage_ansible_playbook_number'
        permissions = (
            ("can_read_ansible_playbook_number", "读取Ansible剧本成员权限"),
            ("can_change_ansible_playbook_number", "更改Ansible剧本成员权限"),
            ("can_add_ansible_playbook_number", "添加Ansible剧本成员权限"),
            ("can_delete_ansible_playbook_number", "删除Ansible剧本成员权限"),
        )
        verbose_name = 'Ansible剧本成员表'
        verbose_name_plural = 'Ansible剧本成员表'

    def __unicode__(self):
        return '%s' % (self.playbook_server)



class Script(models.Model):
    SCRIPT_STATUS=(
        (0,u'未完成'),
        (1,u'已完成'),
    )
    id=models.AutoField(primary_key=True)
    name=models.CharField(max_length=100,default='noName',primary_key=True)
    info=models.CharField(max_length=100,default="noUse")
    script=models.TextField(default='')
    # author = models.ForeignKey(ExtendUser, default=1, related_name='suser')
    status=models.IntegerField(default=0,choices=SCRIPT_STATUS)
    def formatScript(self):
        string=""
        kwargs={}
        for args in self.scriptargs.all():
            kwargs[args.args_name] = args.args_value
        string = string + utils.bash_writer('now',**kwargs)
        string = string + utils.html2bash(self.script)
        return string

class ScriptArgs(models.Model):
    id=models.AutoField(primary_key=True)
    args_name=models.CharField(max_length=100,default='')
    args_value=models.CharField(max_length=100,default='')
    script=models.ForeignKey(Script,default=1,related_name='scriptargs')
