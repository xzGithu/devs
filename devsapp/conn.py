# coding:utf-8
# @Time     :2020/6/28 14:15
# @Author   :Xu Zhe
# @Email    :mistest163@163.com
# @File     :conn.py

import paramiko

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('192.168.181.130', 22, 'root', 'CentOS_73')
stdin, stdout, stderr = ssh.exec_command('hostname')
print stdout.read()