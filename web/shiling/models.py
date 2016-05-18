# coding: utf-8
from __future__ import unicode_literals

from django.db import models

from imagestore.qiniu_manager import url, BUCKET_NAME

import datetime


class Mage(models.Model):

    class Meta(object):
        verbose_name = "法师"
        verbose_name_plural = "法师"

    name = models.CharField(max_length=128, verbose_name="法师名称")
    mage_num = models.CharField(max_length=128, verbose_name="法号")
    cover = models.CharField(max_length=128, verbose_name="头像")
    detail = models.TextField(null=False, verbose_name="简介")
    content = models.TextField(null=False, verbose_name="详情")
    sentiment = models.IntegerField(default=0, verbose_name="人气")

    def __unicode__(self):
        return self.name

    def cover_url(self):
        return url(BUCKET_NAME, self.cover)


class Temple(models.Model):

    class Meta(object):
        verbose_name = "寺庙"
        verbose_name_plural = "寺庙"

    name = models.CharField(max_length=128, verbose_name="名称")
    title = models.CharField(max_length=128, verbose_name="寺庙标题")
    cover = models.CharField(max_length=128, verbose_name="寺庙封面")
    detail = models.TextField(null=False, verbose_name="简介")
    address = models.TextField(null=False, default='', verbose_name="地址")
    content = models.TextField(null=False, verbose_name="详情")
    mage = models.ForeignKey(Mage, blank=True, null=True, verbose_name="主持")

    def __unicode__(self):
        return self.name

    def cover_url(self):
        return url(BUCKET_NAME, self.cover)


class Category(models.Model):

    class Meta(object):
        verbose_name = "供养分类"
        verbose_name_plural = "供养分类"

    name = models.CharField(max_length=128, verbose_name="名称")
    detail = models.TextField(null=False, verbose_name="描述")

    def __unicode__(self):
        return self.name


class Provide(models.Model):

    class Meta(object):
        verbose_name = "供养"
        verbose_name_plural = "供养"

    title = models.CharField(max_length=128, verbose_name="标题")
    subtitle = models.CharField(max_length=300, default='', verbose_name="子标题")
    category = models.ForeignKey(Category, blank=True, null=True, verbose_name="所属分类")
    detail = models.TextField(null=False, verbose_name="描述")
    cover = models.CharField(max_length=128, blank=False, verbose_name="封面图片")
    banner_cover = models.CharField(max_length=128, blank=False, verbose_name="banner图片")
    price = models.FloatField(default=0.0, verbose_name="价格")
    content = models.TextField(null=False, verbose_name="详情")

    def __unicode__(self):
        return self.title

    def cover_url(self):
        return url(BUCKET_NAME, self.cover)

    def banner_cover_url(self):
        return url(BUCKET_NAME, self.banner_cover)


class GoodRaise(models.Model):

    class Meta(object):
        verbose_name = "善筹"
        verbose_name_plural = "善筹"

    title = models.CharField(max_length=128, verbose_name="标题")
    cover = models.CharField(max_length=128, blank=False, verbose_name="封面图片")
    detail = models.TextField(null=False, verbose_name="描述")
    content = models.TextField(null=False, verbose_name="详情")
    total_price = models.FloatField(default=0.0, verbose_name="目标金额")
    start_time = models.DateTimeField(default=datetime.datetime.now, verbose_name="开始时间")
    end_time = models.DateTimeField(default=datetime.datetime.now, verbose_name="结束时间")

    def __unicode__(self):
        return self.title

    def cover_url(self):
        return url(BUCKET_NAME, self.cover)


class Good(models.Model):

    class Meta(object):
        verbose_name = "商品"
        verbose_name_plural = "商品"

    name = models.CharField(max_length=128, verbose_name="名称")
    detail = models.TextField(null=False, verbose_name="描述")
    support_price = models.FloatField(default=0.0, verbose_name="支持金额")
    support_p_count = models.IntegerField(default=0, verbose_name="支持人数")
    goodraise = models.ForeignKey(GoodRaise, blank=True, null=True, verbose_name="所属善筹")

    def __unicode__(self):
        return self.name


class Activity(models.Model):

    class Meta(object):
        verbose_name = "活动"
        verbose_name_plural = "活动"

    name = models.CharField(max_length=128, verbose_name="名称")
    title = models.CharField(max_length=128, verbose_name="标题")
    cover = models.CharField(max_length=128, verbose_name="封面")
    detail = models.TextField(null=False, verbose_name="简介")
    content = models.TextField(null=False, verbose_name="详情")
    address = models.TextField(default='', null=False, verbose_name="地址")
    people_number = models.IntegerField(default=0, verbose_name="活动允许报名人数")
    start_time = models.DateTimeField(default=datetime.datetime.now, verbose_name="开始时间")
    end_time = models.DateTimeField(default=datetime.datetime.now, verbose_name="结束时间")
    views_count = models.IntegerField(default=0, verbose_name="浏览量")

    def __unicode__(self):
        return self.name

    def cover_url(self):
        return url(BUCKET_NAME, self.cover)


class ActivityAttendee(models.Model):

    class Meta(object):
        verbose_name = "活动报名"
        verbose_name_plural = "活动报名"

    name = models.CharField(max_length=128, verbose_name="姓名")
    mobile_phone = models.CharField(max_length=128, verbose_name="手机号码")
    activity = models.ForeignKey(Activity, blank=True, null=True, verbose_name="所属活动")

    def __unicode__(self):
        return self.name


class News(models.Model):

    class Meta(object):
        verbose_name = "新闻"
        verbose_name_plural = "新闻"

    title = models.CharField(max_length=128, verbose_name="标题")
    cover = models.CharField(max_length=128, verbose_name="封面")
    detail = models.TextField(null=False, verbose_name="简介")
    content = models.TextField(null=False, verbose_name="详情")
    start_time = models.DateTimeField(default=datetime.datetime.now, verbose_name="开始时间")
    end_time = models.DateTimeField(default=datetime.datetime.now, verbose_name="结束时间")
    views_count = models.IntegerField(default=0, verbose_name="浏览量")

    def __unicode__(self):
        return self.title

    def cover_url(self):
        return url(BUCKET_NAME, self.cover)


class Volunteer(models.Model):

    class Meta(object):
        verbose_name = "义工"
        verbose_name_plural = "义工"

    title = models.CharField(max_length=128, verbose_name="标题")
    cover = models.CharField(max_length=128, verbose_name="封面")
    detail = models.TextField(null=False, verbose_name="简述")
    content = models.TextField(null=False, verbose_name="详情")
    address = models.TextField(null=False, verbose_name="地址")
    people_number = models.IntegerField(default=0, verbose_name="人数")
    start_time = models.DateTimeField(default=datetime.datetime.now, verbose_name="开始时间")
    end_time = models.DateTimeField(default=datetime.datetime.now, verbose_name="结束时间")
    views_count = models.IntegerField(default=0, verbose_name="浏览量")

    def __unicode__(self):
        return self.title

    def cover_url(self):
        return url(BUCKET_NAME, self.cover)


class VolunteerUser(models.Model):

    class Meta(object):
        verbose_name = "义工报名"
        verbose_name_plural = "义工报名"

    name = models.CharField(max_length=128, verbose_name="姓名")
    mobile_phone = models.CharField(max_length=128, verbose_name="手机号码")
    volunteer = models.ForeignKey(Volunteer, blank=True, null=True, verbose_name="所属义工")

    def __unicode__(self):
        return self.name


class BuddhismKnowledge(models.Model):

    class Meta(object):
        verbose_name = "佛教知识"
        verbose_name_plural = "佛教知识"

    title = models.CharField(max_length=128, verbose_name="标题")
    cover = models.CharField(max_length=128, blank=False, verbose_name="封面图片")
    subtitle = models.TextField(null=False, verbose_name="子标题")
    content = models.TextField(null=False, verbose_name="详情")

    def __unicode__(self):
        return self.title

    def cover_url(self):
        return url(BUCKET_NAME, self.cover)
