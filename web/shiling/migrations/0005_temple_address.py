# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2016-05-03 13:26
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shiling', '0004_auto_20160503_1224'),
    ]

    operations = [
        migrations.AddField(
            model_name='temple',
            name='address',
            field=models.TextField(default='', verbose_name='\u5730\u5740'),
        ),
    ]
