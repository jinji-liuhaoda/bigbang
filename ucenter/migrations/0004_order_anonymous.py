# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2016-05-27 02:35
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ucenter', '0003_order_cuser'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='anonymous',
            field=models.IntegerField(choices=[(0, ''), (1, '')], default=0, verbose_name='\u662f\u5426\u533f\u540d'),
        ),
    ]
