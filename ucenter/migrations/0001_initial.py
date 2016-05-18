# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Cuser',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default='', max_length=128, verbose_name='\u6635\u79f0')),
                ('gender', models.IntegerField(choices=[(0, '\u7537'), (1, '\u5973')], default=0, verbose_name='\u6027\u522b')),
                ('city', models.CharField(blank=True, default='', max_length=128, verbose_name='\u57ce\u5e02')),
                ('phone', models.CharField(blank=True, default='', max_length=128, verbose_name='\u7535\u8bdd')),
                ('province', models.CharField(blank=True, default='', max_length=128, verbose_name='\u7701\u4efd')),
                ('country', models.CharField(blank=True, default='', max_length=128, verbose_name='\u56fd\u5bb6')),
                ('pwd', models.TextField(default='', verbose_name='\u5bc6\u7801')),
                ('openid', models.CharField(blank=True, default='', max_length=128, verbose_name='\u5fae\u4fe1OpenID')),
                ('headimgurl', models.CharField(blank=True, default='', max_length=300, verbose_name='\u5fae\u4fe1\u5934\u50cf')),
                ('created', models.DateTimeField(default=datetime.datetime.now, verbose_name='\u521b\u5efa\u65f6\u95f4')),
            ],
            options={
                'verbose_name': '\u7528\u6237',
                'verbose_name_plural': '\u7528\u6237',
            },
        ),
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
                ('trade_type', models.CharField(default='', max_length=128, verbose_name='\u652f\u4ed8\u7c7b\u578b')),
                ('prepay_id', models.CharField(default='', max_length=300, verbose_name='\u8ba2\u5355id')),
                ('code_url', models.CharField(default='', max_length=300, verbose_name='\u4e8c\u7ef4\u7801\u5730\u5740')),
                ('body', models.CharField(max_length=128, verbose_name='\u63cf\u8ff0')),
                ('detail', models.TextField(verbose_name='\u5546\u54c1\u8be6\u60c5')),
                ('total_fee', models.FloatField(default=0.0, verbose_name='\u603b\u4ef7')),
                ('status', models.IntegerField(choices=[(0, '\u5f85\u4e0b\u5355'), (1, '\u4e0b\u5355\u6210\u529f'), (2, '\u652f\u4ed8\u6210\u529f')], default=0, verbose_name='\u8ba2\u5355\u72b6\u6001')),
                ('from_pay', models.IntegerField(choices=[(0, '\u4f9b\u517b'), (1, '\u5584\u7b79')], default=0, verbose_name='\u8ba2\u5355\u6765\u6e90')),
                ('created', models.DateTimeField(default=datetime.datetime.now, verbose_name='\u521b\u5efa\u65f6\u95f4')),
            ],
            options={
                'verbose_name': '\u8ba2\u5355',
                'verbose_name_plural': '\u8ba2\u5355',
            },
        ),
    ]
