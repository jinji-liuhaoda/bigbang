# coding: utf-8

from django.shortcuts import render, get_object_or_404
from django.template import loader
from django.http import HttpResponse, HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.hashers import make_password, check_password
from shiling.models import (
    Temple,
    Mage,
    Category,
    Provide,
    GoodRaise,
    Good,
    Activity,
    ActivityAttendee,
    News,
    Volunteer,
    VolunteerUser,
    BuddhismKnowledge,
)
from .models import User
from wx_auth import web_webchat_check_login
from settings import UPLOAD_DIR, DOMAIN
import simplejson
import os
import datetime
import time


def index(request):
    user = get_object_or_404(User, id=1)
    activity_attendees = ActivityAttendee.objects.filter(mobile_phone=user.phone)
    request.session['user_id'] = user.id
    context = {
        'title': '揭西石灵寺',
        'user': user,
        'activity_attendees': activity_attendees,
    }
    template = loader.get_template('user.html')
    return HttpResponse(template.render(context, request))


@csrf_exempt
def login(request):
    try:
        request.session['user_id']
        return HttpResponseRedirect('/user/index')
    except Exception, e:
        print e
    error = 0
    if request.method == 'POST':
        phone = request.POST.get('phone', '')
        pwd = request.POST.get('pwd', '')
        try:
            user = get_object_or_404(User, phone=phone)
            is_pwd = check_password(pwd, user.pwd)
            if is_pwd:
                is_validation = 1
            else:
                is_validation = 0
        except User.DoesNotExist:
            is_validation = 0

        if is_validation:
            request.session['user_id'] = user.id
            request.session['openid'] = user.openid
            #获取用户ip
            if request.META.has_key('HTTP_X_FORWARDED_FOR'):
                user_ip = request.META['HTTP_X_FORWARDED_FOR']
            else:
                user_ip = request.META['REMOTE_ADDR']
            request.session['user_ip'] = user_ip
            # 其他页登录需要回调
            redirest = request.session.get('redirest', '')
            if redirest:
                return HttpResponseRedirect(redirest)
            return HttpResponseRedirect('/user/index')
        else:
            error = 1
    context = {
        'title': '揭西石灵寺',
        'error': error,
    }
    template = loader.get_template('login.html')
    return HttpResponse(template.render(context, request))


def login_out(request):
    request.session.flush()
    return HttpResponseRedirect('/user/login')


@web_webchat_check_login
def register_do(request):
    if request.method == 'POST':
        phone = request.POST.get('phone', '')
        pwd = request.POST.get('pwd', '')

        user = User.objects.get(id=request.session.get('user_id', ''))
        user.phone = phone
        user.pwd = make_password(pwd, None, 'pbkdf2_sha256')
        user.save()
        #获取用户ip
        if request.META.has_key('HTTP_X_FORWARDED_FOR'):
            user_ip = request.META['HTTP_X_FORWARDED_FOR']
        else:
            user_ip = request.META['REMOTE_ADDR']
        request.session['user_ip'] = user_ip
        return HttpResponseRedirect('/user/index')

    context = {
        'title': '揭西石灵寺',
        'DOMAIN': DOMAIN,
    }
    template = loader.get_template('register.html')
    return HttpResponse(template.render(context, request))


def register(request):
    request.session['register'] = 1
    return HttpResponseRedirect('/user/register_do')


@csrf_exempt
def pwd_update(request):
    if request.method == 'POST':
        pwd = request.POST.get('pwd1', '')
        try:
            user = get_object_or_404(User, id=request.session['user_id'])
            user.pwd = make_password(pwd, None, 'pbkdf2_sha256')
            user.save()
            return HttpResponseRedirect('/user/index')
        except Exception, e:
            return HttpResponseRedirect('/user/login')
    context = {
        'title': '揭西石灵寺',
    }
    template = loader.get_template('pwd_update.html')
    return HttpResponse(template.render(context, request))


@web_webchat_check_login
def wx_login():
    return HttpResponseRedirect('/user/login')


def wx_pay():
    return 1


def ch_phone(request, phone):
    users = User.objects.filter(phone=phone)
    if len(users):
        return True
    else:
        return False


def check_phone(request, phone):
    cp = ch_phone(request, phone)
    if cp:
        return HttpResponse(simplejson.dumps({'error': 1, 'msg': '该手机号码已注册,请登录'}, ensure_ascii = False))
    else:
        return HttpResponse(simplejson.dumps({'error': 0, 'msg': ''}, ensure_ascii=False))
