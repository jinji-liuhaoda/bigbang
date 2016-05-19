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
    url(r'^$', temple_view.index, name='temple_index'),

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

    # 揭西石灵寺管理后台
    url(r'^admin/login$', admin_views.login_view),
    url(r'^admin/logout$', admin_views.logout_view),
    url(r'^admin/$', admin_views.index),

    # 关于寺庙
    url(r'^admin/temple$', admin_views.temple_edit),

    # 法师列表
    url(r'^admin/mage$', admin_views.mage_list),
    url(r'^admin/mage/create$', admin_views.mage_create),
    url(r'^admin/mage/(?P<mage_id>\d+)/edit$', admin_views.mage_edit),
    url(r'^admin/mage/(?P<mage_id>\d+)/delete$', admin_views.mage_delete),

    # 供养
    url(r'^admin/gooddeedday$', admin_views.gooddeedday_detail),
    url(r'^admin/category$', admin_views.category_list),
    url(r'^admin/category/create$', admin_views.category_create),
    url(r'^admin/category/(?P<category_id>\d+)/edit$', admin_views.category_edit),
    url(r'^admin/category/(?P<category_id>\d+)/delete$', admin_views.category_delete),

    url(r'^admin/provide$', admin_views.provide_list),
    url(r'^admin/provide/create$', admin_views.provide_create),
    url(r'^admin/provide/(?P<provide_id>\d+)/edit$', admin_views.provide_edit),

    url(r'^admin/provide-pay$', admin_views.provide_pay_list),

    # 善筹
    url(r'^admin/(?P<goodraise_id>\d+)/good$', admin_views.good_list),
    url(r'^admin/good/(?P<goodraise_id>\d+)/create$', admin_views.good_create),
    url(r'^admin/good/(?P<good_id>\d+)/edit$', admin_views.good_edit),
    url(r'^admin/good/(?P<good_id>\d+)/delete$', admin_views.good_delete),
    url(r'^admin/goodraise$', admin_views.goodraise_list),
    url(r'^admin/goodraise/create$', admin_views.goodraise_create),
    url(r'^admin/goodraise/(?P<goodraise_id>\d+)/edit$', admin_views.goodraise_edit),

    url(r'^admin/goodraise-pay$', admin_views.goodraise_pay_list),

    # 活动
    url(r'^admin/activity$', admin_views.activity_list),
    url(r'^admin/activity/create$', admin_views.activity_create),
    url(r'^admin/activity/(?P<activity_id>\d+)/edit$', admin_views.activity_edit),
    url(r'^admin/activity/(?P<activity_id>\d+)/delete$', admin_views.activity_delete),

    url(r'^admin/(?P<activity_id>\d+)/activityattendee$', admin_views.activity_attendee_list),
    url(r'^admin/activityattendee/(?P<activityattendee_id>\d+)/edit$', admin_views.activityattendee_edit),
    url(r'^admin/activityattendee/(?P<activityattendee_id>\d+)/delete$', admin_views.activityattendee_delete),

    # 新闻
    url(r'^admin/news$', admin_views.news_list),
    url(r'^admin/news/create$', admin_views.news_create),
    url(r'^admin/news/(?P<news_id>\d+)/edit$', admin_views.news_edit),
    url(r'^admin/news/(?P<news_id>\d+)/delete$', admin_views.news_delete),

    # 义工
    url(r'^admin/volunteer$', admin_views.volunteer_detail),
    url(r'^admin/(?P<volunteer_id>\d+)/volunteeruser$', admin_views.volunteeruser_list),
    url(r'^admin/volunteeruser/(?P<volunteeruser_id>\d+)/edit$', admin_views.volunteeruser_edit),
    url(r'^admin/volunteeruser/(?P<volunteeruser_id>\d+)/delete$', admin_views.volunteeruser_delete),

    # 佛法知识
    url(r'^admin/buddhismknowledge$', admin_views.buddhismknowledge_list),
    url(r'^admin/buddhismknowledge/create$', admin_views.buddhismknowledge_create),
    url(r'^admin/buddhismknowledge/(?P<buddhismknowledge_id>\d+)/edit$', admin_views.buddhismknowledge_edit),
    url(r'^admin/buddhismknowledge/(?P<buddhismknowledge_id>\d+)/delete$', admin_views.buddhismknowledge_delete),

    # 用户管理
    url(r'^admin/cuser$', admin_views.cuser_list),
    url(r'^admin/cuser/create$', admin_views.cuser_create),
    url(r'^admin/cuser/(?P<cuser_id>\d+)/edit$', admin_views.cuser_edit),
    url(r'^admin/cuser/(?P<cuser_id>\d+)/delete$', admin_views.cuser_delete),

    # 管理员
    url(r'^admin/user$', admin_views.user_list),
    url(r'^admin/user/create$', admin_views.user_create),
    url(r'^admin/user/(?P<user_id>\d+)/edit$', admin_views.user_edit),
    url(r'^admin/user/(?P<user_id>\d+)/delete$', admin_views.user_delete),

    # django后台
    url(r'^superadmin/', admin.site.urls),

    # 用户中心
    url(r'^cuser/', include('ucenter.urls')),

    # 后台上传
    url(r'^admin/ckeditor_upload', admin_views.ckeditor_upload, name='admin_upload'),
]
