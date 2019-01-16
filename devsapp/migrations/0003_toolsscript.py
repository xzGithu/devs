# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2018-04-08 10:13
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('devsapp', '0002_script_id'),
    ]

    operations = [
        migrations.CreateModel(
            name='ToolsScript',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, verbose_name='\u5de5\u5177\u540d\u79f0')),
                ('tool_script', models.TextField(verbose_name='\u811a\u672c')),
                ('tool_run_type', models.IntegerField(choices=[(0, 'shell'), (1, 'python'), (2, 'yml')], default=0, verbose_name='\u811a\u672c\u7c7b\u578b')),
                ('comment', models.TextField(blank=True, null=True, verbose_name='\u5de5\u5177\u8bf4\u660e')),
                ('ctime', models.DateTimeField(auto_now_add=True, null=True, verbose_name='\u521b\u5efa\u65f6\u95f4')),
                ('utime', models.DateTimeField(auto_now=True, null=True, verbose_name='\u66f4\u65b0\u65f6\u95f4')),
            ],
            options={
                'db_table': 'ToolsScript',
                'verbose_name': '\u5de5\u5177',
                'verbose_name_plural': '\u5de5\u5177',
            },
        ),
    ]
