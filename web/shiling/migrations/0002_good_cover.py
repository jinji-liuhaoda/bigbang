# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2016-05-29 07:57
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shiling', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='good',
            name='cover',
            field=models.CharField(default='', max_length=128, verbose_name='\u5c01\u9762\u56fe\u7247'),
        ),
    ]
