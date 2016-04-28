# coding: utf-8

from django.conf.urls import url
from django.contrib import admin
from shiling import (
    temple_view,
    admin_views,
    auth_views,
)

admin.autodiscover()
urlpatterns = [
    # 首页
    url(r'^index$', temple_view.index, name='temple_index'),

    # 供养
    url(r'^provide/$', temple_view.provide_list, name='provide_list'),
    url(r'^provide/(?P<provide_id>\d+)/$', temple_view.provide_detail, name='provide_detail'),

    # 善筹
    url(r'^goodraise/$', temple_view.goodraise_list, name='goodraise_list'),
    url(r'^goodraise/(?P<goodraise_id>\d+)/$', temple_view.goodraise_detail, name='goodraise_detail'),

    # 祈福
    url(r'^blessing/$', temple_view.blessing_list, name='blessing_list'),

    # 活动
    url(r'^activity/$', temple_view.activity_list, name='activity_list'),
    url(r'^activity/(?P<activity_id>\d+)/$', temple_view.activity_detail, name='activity_detail'),
    url(r'^activity/(?P<activity_id>\d+)/signup$', temple_view.activity_signup, name='activity_signup'),

    # 新闻
    url(r'^news/$', temple_view.news_list, name='news_list'),
    url(r'^news/(?P<activity_id>\d+)/$', temple_view.news_detail, name='news_detail'),

    # 义工
    url(r'^volunteer/$', temple_view.volunteer_detail, name='volunteer_detail'),
    url(r'^volunteer/(?P<volunteer_id>\d+)/signup$', temple_view.volunteer_signup, name='volunteer_signup'),

    # 佛教知识
    url(r'^buddhismknowledge/$', temple_view.buddhismknowledge_list, name='buddhismknowledge_list'),
    url(r'^buddhismknowledge/(?P<buddhismknowledge_id>\d+)/$', temple_view.buddhismknowledge_detail, name='buddhismknowledge_detail'),

    # 捐赠
    url(r'^donation/(?P<donation_type>\w+)/(?P<donation_amount>\w+)/add$', temple_view.donation_add, name='donation_add'),

    # 主持详情
    url(r'^host/$', temple_view.host_detail, name='host_detail'),

    # 微信网页授权
    # url(r'^wechat/login/$', auth_views.wechat_login, name='wechat_login'),
    # url(r'^wechat/do_login/$', auth_views.wechat_do_login, name='wechat_do_login'),

    #支付
    url(r'^pay/(?P<pay_type>\d+)/(?P<donation_amount>\w+)/add$', temple_view.pay_add, name='pay_add'),

    # 后台
    # url(r'^admin/', admin_views.index),
    url(r'^superadmin/', admin.site.urls),

    # 后台上传
    url(r'^admin/upload$', admin_views.upload, name='upload'),
]
