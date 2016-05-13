# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2016-05-11 07:16
from __future__ import unicode_literals

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ucenter', '0003_user_pwd'),
    ]

    operations = [
        migrations.CreateModel(
            name='GoodId',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
            options={
                'verbose_name': '\u5546\u54c1id',
                'verbose_name_plural': '\u5546\u54c1id',
            },
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('out_trade_no', models.CharField(max_length=128, verbose_name='\u8ba2\u5355\u53f7')),
                ('product_id', models.CharField(max_length=128, verbose_name='\u5546\u54c1id')),
                ('body', models.CharField(max_length=128, verbose_name='\u63cf\u8ff0')),
                ('detail', models.TextField(verbose_name='\u5546\u54c1\u8be6\u60c5')),
                ('total_fee', models.FloatField(default=0.0, verbose_name='\u603b\u4ef7')),
                ('status', models.IntegerField(choices=[(0, '\u5f85\u4e0b\u5355'), (1, '\u4e0b\u5355\u6210\u529f'), (2, '\u652f\u4ed8\u6210\u529f')], default=0, verbose_name='\u8ba2\u5355\u72b6\u6001')),
                ('created', models.DateTimeField(default=datetime.datetime.now, verbose_name='\u521b\u5efa\u65f6\u95f4')),
            ],
            options={
                'verbose_name': '\u8ba2\u5355',
                'verbose_name_plural': '\u8ba2\u5355',
            },
        ),
    ]