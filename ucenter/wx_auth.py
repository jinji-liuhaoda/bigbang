# coding: utf-8

from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect
from settings import DOMAIN
from functools import wraps
from .constants import WX_APP_ID, WX_SECRET, USE_FAKE_WECHAT_USER, WX_REDIRECT_URI, WX_GET_ACCESS_TOKEN_URL, WX_AUTH_URL

from .models import Cuser
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

        cuser_id = request.session.get('cuser_id', 0)
        openid = request.session.get('openid', '')
        cnt = Cuser.objects.filter(id=cuser_id, openid=openid)
        if not openid:
            request.session['red_next_url'] = request.get_raw_uri()
            return HttpResponseRedirect(WX_AUTH_URL)

        return view(request, *args, **kwargs)

    return wrapper


def wechat_do_login(request):
    # 获取access_token
    data = get_data(request.GET.get('code', ''))
    openid = data.get('openid', '')
    register = request.session.get('register', 0)
    if register:
        request.session['register'] = False
    else:
        cuser, _ = Cuser.objects.get_or_create(openid=openid)
        # 设置Session
        request.session['cuser_id'] = cuser.id
    print 'wechat_do_login', openid

    # 设置Session
    request.session['openid'] = openid
    # 获取用户ip
    if 'HTTP_X_FORWARDED_FOR' in request.META:
        cuser_ip = request.META['HTTP_X_FORWARDED_FOR']
    else:
        cuser_ip = request.META['REMOTE_ADDR']
    request.session['cuser_ip'] = cuser_ip
    red_next_url = request.session.get('red_next_url', '')
    if not red_next_url:
        red_next_url = '/cuser/index'
    return HttpResponseRedirect(red_next_url)


def make_fake_user(request):
    openid = 'attackt'
    phone = '12345678901'
    cuser, _ = Cuser.objects.get_or_create(openid=openid, phone=phone)
    request.session['openid'] = openid
    request.session['cuser_id'] = cuser.id
