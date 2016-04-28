# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2016-04-27 10:43
from __future__ import unicode_literals

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('shiling', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Activity',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=128, verbose_name='\u540d\u79f0')),
                ('title', models.CharField(max_length=128, verbose_name='\u6807\u9898')),
                ('cover', models.CharField(max_length=128, verbose_name='\u5c01\u9762')),
                ('detail', models.TextField(verbose_name='\u7b80\u4ecb')),
                ('content', models.TextField(verbose_name='\u5730\u5740')),
                ('people_number', models.IntegerField(default=0, verbose_name='\u4eba\u6570')),
                ('start_time', models.DateTimeField(default=datetime.datetime.now, verbose_name='\u5f00\u59cb\u65f6\u95f4')),
                ('start_end', models.DateTimeField(default=datetime.datetime.now, verbose_name='\u7ed3\u675f\u65f6\u95f4')),
                ('views_count', models.IntegerField(default=0, verbose_name='\u6d4f\u89c8\u91cf')),
            ],
            options={
                'verbose_name': '\u6d3b\u52a8',
                'verbose_name_plural': '\u6d3b\u52a8',
            },
        ),
        migrations.CreateModel(
            name='ActivityUser',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=128, verbose_name='\u59d3\u540d')),
                ('mobile_phone', models.CharField(max_length=128, verbose_name='\u624b\u673a\u53f7\u7801')),
                ('activity', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='shiling.Activity', verbose_name='\u6240\u5c5e\u6d3b\u52a8')),
            ],
            options={
                'verbose_name': '\u6d3b\u52a8\u62a5\u540d',
                'verbose_name_plural': '\u6d3b\u52a8\u62a5\u540d',
            },
        ),
        migrations.CreateModel(
            name='BuddhismKnowledge',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=128, verbose_name='\u6807\u9898')),
                ('cover', models.CharField(max_length=128, verbose_name='\u5c01\u9762\u56fe\u7247')),
                ('detail', models.TextField(verbose_name='\u5b50\u6807\u9898')),
                ('content', models.TextField(verbose_name='\u8be6\u60c5')),
            ],
            options={
                'verbose_name': '\u4f5b\u6559\u77e5\u8bc6',
                'verbose_name_plural': '\u4f5b\u6559\u77e5\u8bc6',
            },
        ),
        migrations.CreateModel(
            name='GoodRaise',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=128, verbose_name='\u6807\u9898')),
                ('cover', models.CharField(max_length=128, verbose_name='\u5c01\u9762\u56fe\u7247')),
                ('detail', models.TextField(verbose_name='\u63cf\u8ff0')),
                ('content', models.TextField(verbose_name='\u8be6\u60c5')),
                ('total_price', models.FloatField(default=0.0, verbose_name='\u76ee\u6807\u91d1\u989d')),
                ('start_time', models.DateTimeField(default=datetime.datetime.now, verbose_name='\u5f00\u59cb\u65f6\u95f4')),
                ('start_end', models.DateTimeField(default=datetime.datetime.now, verbose_name='\u7ed3\u675f\u65f6\u95f4')),
            ],
            options={
                'verbose_name': '\u5584\u7b79',
                'verbose_name_plural': '\u5584\u7b79',
            },
        ),
        migrations.CreateModel(
            name='Goods',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=128, verbose_name='\u540d\u79f0')),
                ('detail', models.TextField(verbose_name='\u63cf\u8ff0')),
                ('support_price', models.FloatField(default=0.0, verbose_name='\u652f\u6301\u91d1\u989d')),
                ('support_p_count', models.IntegerField(default=0, verbose_name='\u652f\u6301\u4eba\u6570')),
                ('goodraise', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='shiling.GoodRaise', verbose_name='\u6240\u5c5e\u5584\u7b79')),
            ],
            options={
                'verbose_name': '\u5546\u54c1',
                'verbose_name_plural': '\u5546\u54c1',
            },
        ),
        migrations.CreateModel(
            name='Mage',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=128, verbose_name='\u6cd5\u5e08\u540d\u79f0')),
                ('mage_num', models.CharField(max_length=128, verbose_name='\u6cd5\u53f7')),
                ('cover', models.CharField(max_length=128, verbose_name='\u5934\u50cf')),
                ('detail', models.TextField(verbose_name='\u7b80\u4ecb')),
                ('content', models.TextField(verbose_name='\u8be6\u60c5')),
            ],
            options={
                'verbose_name': '\u6cd5\u5e08',
                'verbose_name_plural': '\u6cd5\u5e08',
            },
        ),
        migrations.CreateModel(
            name='News',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=128, verbose_name='\u6807\u9898')),
                ('cover', models.CharField(max_length=128, verbose_name='\u5c01\u9762')),
                ('detail', models.TextField(verbose_name='\u7b80\u4ecb')),
                ('content', models.TextField(verbose_name='\u8be6\u60c5')),
                ('start_time', models.DateTimeField(default=datetime.datetime.now, verbose_name='\u5f00\u59cb\u65f6\u95f4')),
                ('start_end', models.DateTimeField(default=datetime.datetime.now, verbose_name='\u7ed3\u675f\u65f6\u95f4')),
                ('views_count', models.IntegerField(default=0, verbose_name='\u6d4f\u89c8\u91cf')),
            ],
            options={
                'verbose_name': '\u65b0\u95fb',
                'verbose_name_plural': '\u65b0\u95fb',
            },
        ),
        migrations.CreateModel(
            name='Temple',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=128, verbose_name='\u540d\u79f0')),
                ('title', models.CharField(max_length=128, verbose_name='\u5bfa\u5e99\u6807\u9898')),
                ('cover', models.CharField(max_length=128, verbose_name='\u5bfa\u5e99\u5c01\u9762')),
                ('detail', models.TextField(verbose_name='\u7b80\u4ecb')),
                ('content', models.TextField(verbose_name='\u8be6\u60c5')),
                ('mage', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='shiling.Mage', verbose_name='\u4e3b\u6301')),
            ],
            options={
                'verbose_name': '\u5bfa\u5e99',
                'verbose_name_plural': '\u5bfa\u5e99',
            },
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=128, verbose_name='\u59d3\u540d')),
                ('gender', models.IntegerField(choices=[(0, '\u7537'), (1, '\u5973')], default=0, verbose_name='\u6027\u522b')),
                ('openid', models.CharField(blank=True, max_length=128, verbose_name='\u5fae\u4fe1OpenID')),
                ('headimgurl', models.CharField(blank=True, max_length=300, verbose_name='\u5fae\u4fe1\u5934\u50cf')),
                ('scanner_id', models.CharField(blank=True, max_length=128, verbose_name='Scanner ID')),
                ('created', models.DateTimeField(default=datetime.datetime.now, verbose_name='\u521b\u5efa\u65f6\u95f4')),
            ],
            options={
                'verbose_name': '\u7528\u6237',
                'verbose_name_plural': '\u7528\u6237',
            },
        ),
        migrations.CreateModel(
            name='Volunteers',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=128, verbose_name='\u6807\u9898')),
                ('cover', models.CharField(max_length=128, verbose_name='\u5c01\u9762')),
                ('detail', models.TextField(verbose_name='\u7b80\u8ff0')),
                ('content', models.TextField(verbose_name='\u5730\u5740')),
                ('people_number', models.IntegerField(default=0, verbose_name='\u4eba\u6570')),
                ('start_time', models.DateTimeField(default=datetime.datetime.now, verbose_name='\u5f00\u59cb\u65f6\u95f4')),
                ('start_end', models.DateTimeField(default=datetime.datetime.now, verbose_name='\u7ed3\u675f\u65f6\u95f4')),
                ('views_count', models.IntegerField(default=0, verbose_name='\u6d4f\u89c8\u91cf')),
            ],
            options={
                'verbose_name': '\u4e49\u5de5',
                'verbose_name_plural': '\u4e49\u5de5',
            },
        ),
        migrations.CreateModel(
            name='VolunteersUser',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=128, verbose_name='\u59d3\u540d')),
                ('mobile_phone', models.CharField(max_length=128, verbose_name='\u624b\u673a\u53f7\u7801')),
                ('volunteers', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='shiling.Volunteers', verbose_name='\u6240\u5c5e\u4e49\u5de5')),
            ],
            options={
                'verbose_name': '\u4e49\u5de5\u62a5\u540d',
                'verbose_name_plural': '\u4e49\u5de5\u62a5\u540d',
            },
        ),
        migrations.AlterField(
            model_name='provide',
            name='title',
            field=models.CharField(max_length=128, verbose_name='\u6807\u9898'),
        ),
    ]
