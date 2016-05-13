# coding: utf-8

from django.shortcuts import render
from django.http import HttpResponseRedirect
from settings import DOMAIN
from functools import wraps
from .constants import WX_APP_ID, WX_SECRET, USE_FAKE_WECHAT_USER, WX_REDIRECT_URI, WX_GET_ACCESS_TOKEN_URL, WX_AUTH_URL

from .models import User
import requests


def get_data(code):
    r = requests.get(WX_GET_ACCESS_TOKEN_URL.format(
        WX_APP_ID, WX_SECRET, code
    ))

    data = r.json()
    return data


def web_webchat_check_login(view):
    @wraps(view)
    def wrapper(request, *args, **kwargs):
        if USE_FAKE_WECHAT_USER:
            make_fake_user(request)
            return view(request, *args, **kwargs)

        user_id = request.session.get('user_id', '')
        openid = request.session.get('openid', '')
        cnt = User.objects.filter(id=user_id, openid=openid)
        if not user_id or not openid or not cnt:
            request.session['red_next_url'] = request.get_raw_uri()
            return HttpResponseRedirect(WX_AUTH_URL)

        return view(request, *args, **kwargs)

    return wrapper


def wechat_do_login(request):
    # 获取access_token
    data = get_data(request.GET.get('code', ''))
    openid = data.get('openid', '')
    register = request.session.get('register', '')
    if register:
        request.session['register'] = False
    else:
        user, _ = User.objects.get_or_create(openid=openid)

    print 'wechat_do_login', openid, user.id

    # 设置Session
    request.session['openid'] = openid
    request.session['user_id'] = user.id
    # 获取用户ip
    if request.META.has_key('HTTP_X_FORWARDED_FOR'):
        user_ip = request.META['HTTP_X_FORWARDED_FOR']
    else:
        user_ip = request.META['REMOTE_ADDR']
    request.session['user_ip'] = user_ip
    red_next_url = request.session.get('red_next_url', '')

    return HttpResponseRedirect(red_next_url)


def make_fake_user(request):
    openid = 'attackt'
    phone = '12345678901'
    user, _ = User.objects.get_or_create(openid=openid, phone=phone)
    request.session['openid'] = openid
    request.session['user_id'] = user.id
