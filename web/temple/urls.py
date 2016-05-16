# coding: utf-8

from django.conf.urls import url, include
from django.contrib import admin
from shiling import (
    temple_view,
    admin_views,
)

admin.autodiscover()
urlpatterns = [
    # 首页
    url(r'^index/$', temple_view.index, name='temple_index'),

    # 供养
    url(r'^provide/$', temple_view.provide_list, name='provide_list'),
    url(r'^provide/(?P<provide_id>\d+)$', temple_view.provide_detail, name='provide_detail'),
    url(r'^provide_pay/(?P<provide_id>\d+)$', temple_view.provide_pay, name='provide_pay'),

    # 善筹
    url(r'^goodraise/$', temple_view.goodraise_list, name='goodraise_list'),
    url(r'^goodraise/(?P<goodraise_id>\d+)$', temple_view.goodraise_detail, name='goodraise_detail'),
    url(r'^good_pay/(?P<good_id>\d+)$', temple_view.good_pay, name='good_pay'),

    # 祈福
    url(r'^blessing/$', temple_view.blessing_list, name='blessing_list'),

    # 活动
    url(r'^activity/$', temple_view.activity_list, name='activity_list'),
    url(r'^activity/(?P<activity_id>\d+)$', temple_view.activity_detail, name='activity_detail'),
    url(r'^activity/(?P<activity_id>\d+)/signup$', temple_view.activity_signup, name='activity_signup'),
    url(r'^views_count/(?P<activity_id>\d+)$', temple_view.views_count, name='views_count'),

    # 新闻
    url(r'^news/$', temple_view.news_list, name='news_list'),
    url(r'^news/(?P<news_id>\d+)$', temple_view.news_detail, name='news_detail'),
    url(r'^views_count_news/(?P<news_id>\d+)$', temple_view.views_count_news, name='views_count_news'),

    # 义工
    url(r'^volunteer/$', temple_view.volunteer_detail, name='volunteer_detail'),
    url(r'^volunteer/(?P<volunteer_id>\d+)/signup$', temple_view.volunteer_signup, name='volunteer_signup'),
    url(r'^views_count_volunteer/(?P<volunteer_id>\d+)$', temple_view.views_count_volunteer, name='views_count_volunteer'),

    # 佛教知识
    url(r'^buddhismknowledge/$', temple_view.buddhismknowledge_list, name='buddhismknowledge_list'),
    url(r'^buddhismknowledge/(?P<buddhismknowledge_id>\d+)$', temple_view.buddhismknowledge_detail, name='buddhismknowledge_detail'),

    # 主持详情
    url(r'^host_detail/(?P<host_id>\d+)$', temple_view.host_detail, name='host_detail'),
    url(r'^sentiment/(?P<host_id>\d+)$', temple_view.sentiment, name='sentiment'),

    # 后台
    # url(r'^admin/', admin_views.index),
    url(r'^admin/', admin.site.urls),
    # 用户中心
    url(r'^user/', include('ucenter.urls')),

    # 后台上传
    url(r'^admin/upload$', admin_views.upload, name='upload'),
]
