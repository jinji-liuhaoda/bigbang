# coding: utf-8


from __future__ import unicode_literals

from django.db import models

import datetime


class User(models.Model):

    class Meta(object):
        verbose_name = "用户"
        verbose_name_plural = "用户"

    GENDER_CHOICES = (
        (0, '男'),
        (1, '女'),
    )

    name = models.CharField(max_length=128, verbose_name="昵称")
    gender = models.IntegerField(choices=GENDER_CHOICES, default=0, verbose_name="性别")
    city = models.CharField(max_length=128, blank=True, verbose_name="城市")
    phone = models.CharField(max_length=128, blank=True, verbose_name="电话")
    province = models.CharField(max_length=128, blank=True, verbose_name="省份")
    country = models.CharField(max_length=128, blank=True, verbose_name="国家")
    pwd = models.TextField(null=False, default='', verbose_name="密码")
    openid = models.CharField(max_length=128, blank=True, verbose_name="微信OpenID")
    headimgurl = models.CharField(max_length=300, blank=True, verbose_name="微信头像")
    created = models.DateTimeField(default=datetime.datetime.now, verbose_name="创建时间")

    def __unicode__(self):
        return self.name


class Order(models.Model):

    class Meta(object):
        verbose_name = "订单"
        verbose_name_plural = "订单"

    GENDER_CHOICES = (
        (0, '待下单'),
        (1, '下单成功'),
        (2, '支付成功'),
    )

    out_trade_no = models.CharField(max_length=128, verbose_name="订单号")
    product_id = models.CharField(max_length=128, verbose_name="商品id")
    trade_type = models.CharField(max_length=128, default='', verbose_name="支付类型")
    prepay_id = models.CharField(max_length=300, default='', verbose_name="订单id")
    code_url = models.CharField(max_length=300, default='', verbose_name="二维码地址")
    body = models.CharField(max_length=128, verbose_name="描述")
    detail = models.TextField(null=False, verbose_name="商品详情")
    total_fee = models.FloatField(default=0.0, verbose_name="总价")
    status = models.IntegerField(choices=GENDER_CHOICES, default=0, verbose_name="订单状态")
    created = models.DateTimeField(default=datetime.datetime.now, verbose_name="创建时间")

    def __unicode__(self):
        return self.body


class GoodId(models.Model):
    class Meta(object):
        verbose_name = "商品id"
        verbose_name_plural = "商品id"
