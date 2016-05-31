# coding: utf-8

from django.conf.urls import url

from ucenter import auth_views, wx_auth, wx_pay

urlpatterns = [
    # 用户中心
    url(r'^login/$', auth_views.login, name='login'),
    url(r'^retrieve/$', auth_views.retrieve, name='retrieve'),
    url(r'^login_out/$', auth_views.login_out, name='login_out'),
    url(r'^register/$', auth_views.register, name='register'),
    url(r'^register_do/$', auth_views.register_do, name='register_do'),
    url(r'^index$', auth_views.index, name='index'),
    url(r'^pwd_update/$', auth_views.pwd_update, name='pwd_update'),
    url(r'^retrieve_pwd/$', auth_views.retrieve_pwd, name='retrieve_pwd'),
    url(r'^phone/(?P<phone>\d+)$', auth_views.check_phone, name='check_phone'),
    url(r'^send_code/(?P<phone>\d+)$', auth_views.send_code, name='send_code'),
    # 微信相关
    url(r'^wx_login/$', auth_views.wx_login, name='wx_login'),
    url(r'^wechat_do_login/$', wx_auth.wechat_do_login, name='wechat_do_login'),
    url(r'^wx_create_order/$', wx_pay.create_order, name='create_order'),

    # 支付成功后微信回调地址
    url(r'^wx_callback_pay/$', wx_pay.wx_callback_pay, name='wx_callback_pay'),
]
