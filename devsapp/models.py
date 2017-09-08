# -*-coding:utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User

# Create your models here.

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
    state = models.IntegerField(default=0)

    def __unicode__(self):
        return u'%s' % self.host

#建立职员模型，这是对内置user表的扩展
# class Employee(models.Model):
#     #对应User表，建立一对一的模型，目的是更好地扩展而不影响原user表结构
#     user = models.OneToOneField(User, on_delete=models.CASCADE)
#     #定义user的职责
#     responsibility = models.CharField(max_length=100,blank=True)
#
#     def __unicode__(self):
#         return self.user.username
# #建立任务表
# class Task(models.Model):
#     #执行的任务和人员关系是多对多的关系
#     task_member = models.ManyToManyField(Employee)
#     #为任务类型分类
#     category = (
#         (U'综合事务','综合事务'),
#         (U'机构建设','机构建设'),
#         (U'线路事务','线路事务'),
#     )
#     #任务的流水号
#     task_code = models.CharField(max_length=30, default='error_code')
#     #任务的名称
#     task_title = models.CharField(verbose_name='任务名称',max_length=100)
#     #任务的分类
#     task_category = models.CharField(verbose_name='任务分类',max_length=100,choices=category,default='综合事务')
#     #任务的联系人
#     task_contacts = models.TextField(verbose_name='联系人',blank=True)
#     #任务状态
#     task_status = models.CharField(verbose_name='处理中',max_length=20,default='处理中')
#     #任务登记人
#     task_signer = models.CharField(max_length=30,default='system')
#     #任务登记时间
#     task_signtime = models.DateField(auto_now_add=True)
#
#     def __unicode__(self):
#         return self.task_title
#
# #建立实施步骤
# class Process(models.Model):
#     #与task表格是一对多的关系，依附于task之上
#     task = models.ForeignKey(Task)
#     #实施步骤内容
#     process_content = models.TextField(blank=True)
#     #实施步骤登记时间
#     process_signtime = models.DateTimeField(auto_now_add=True)
#     #实施步骤登记人
#     process_signer = models.CharField(max_length=30,default='system')
#
#     def __unicode__(self):
#         return self.process_content
#
# #上传附件
# class Upload(models.Model):
#     #与task表格是一对多的关系，依附于task之上
#     task = models.ForeignKey(Task)
#     #上传附件名称
#     upload_title = models.CharField(max_length=255)
#     #上传附件路径
#     upload_path = models.CharField(max_length=255)
#     #上传附件时间
#     upload_signtime = models.DateTimeField(auto_now_add=True,null=True)
#
#     def __unicode__(self):
#         return self.upload_title

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
    def __unicode__(self):
        return self.ip
