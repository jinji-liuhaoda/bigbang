# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2016-05-09 06:12
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shiling', '0009_provide_subtitle'),
    ]

    operations = [
        migrations.AlterField(
            model_name='provide',
            name='subtitle',
            field=models.CharField(default='', max_length=300, verbose_name='\u5b50\u6807\u9898'),
        ),
    ]