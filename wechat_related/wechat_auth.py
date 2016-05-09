# coding: utf-8

from django.shortcuts import render
from django.http import HttpResponseRedirect

import requests
from functools import wraps

from settings import (
    MAKE_FAKE_WECHAT_USER,
    WX_AUTH_URL
)


def get_openid(code):
    r = requests.get(WX_GET_ACCESS_TOKEN_URL.format(
        WX_APP_ID, WX_SECRET, code
    ))

    data = r.json()
    return = data.get('openid', '')


def check_login(view):
    @wrap(view)
    def wrapper(request, *args, **kwargs):
        if USE_FAKE_WECHAT_USER:
            make_fake_user(request)
            return view(request, *args, **kwargs)

        user_id = request.session.get('user_id', 0)
        openid = request.session.get('openid', '')

        cnt = User.objects.filter(id=user_id, openid=openid)

        if not user_id or not openid or not cnt:

            return HttpResponseRedirect('/ucenter/register')

        return view(request, *args, **kwargs)

    return wrapper


def register(request):
    if request.method == 'POST':
        action = request.POST.get('action', '')
        if action == 'get_sms':
            pass
        if action == 'get_openid':
            return HttpResponseRedirect(WX_AUTH_URL)

    if request.method == 'GET':
        code = request.GET.get('code', '')
        if not code:
            return render(request, 'register.html')
        else:
            openid = get_openid(code)
            mobile = request.GET.get('mobile', '')

            user, _ = User.objects.get_or_create(openid=openid, mobile=mobile)

            request.session['openid'] = openid
            request.session['user_id'] = user.id

            name = request.session.get('name', '')
            if name == 'user_activitiy':
                redirect_uri = '/ucenter/{}/activity'.format(user.id)
            elif name == 'user_grade':
                redirect_uri = '/ucenter/{}/grade'.format(user.id)
            elif name == 'user_score':
                redirect_uri = '/ucenter/{}/score'.format(user.id)
            else:
                redirect_uri = name

            return HttpResponseRedirect(redirect_uri)


def make_fake_user(request):
    openid = 'attackt'
    mobile = '12345678901'
    user, _ = User.objects.get_or_create(openid=openid, mobile=mobile)
    request.session['openid'] = openid
    request.session['user_id'] = user.id

    return
