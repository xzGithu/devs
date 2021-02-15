# coding:utf-8
# @Time     :2020/6/27 16:43
# @Author   :Xu Zhe
# @Email    :mistest163@163.com
# @File     :autodeploy.py

from rest_framework import mixins
from rest_framework import generics

from operation.utils import ansible_python2

def autoDeploy(request):
    if request.method == 'POST':
        hostlist = request.POST.get('hostlists')

        pass