# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2020-12-27 14:36
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('devsapp', '0008_history_history_str_history_text_history_uint'),
    ]

    operations = [
        migrations.AlterField(
            model_name='history_text',
            name='uint',
            field=models.CharField(max_length=10),
        ),
        migrations.AlterField(
            model_name='history_uint',
            name='uint',
            field=models.CharField(max_length=10),
        ),
    ]
