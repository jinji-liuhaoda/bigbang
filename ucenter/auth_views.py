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
from .models import Cuser
from wx_auth import web_webchat_check_login
from settings import UPLOAD_DIR, DOMAIN
import simplejson
import os
import datetime
import time


def index(request):
    cuser = get_object_or_404(Cuser, id=request.session['cuser_id'])
    activity_attendees = ActivityAttendee.objects.filter(mobile_phone=cuser.phone)
    request.session['cuser_id'] = cuser.id
    context = {
        'title': '揭西石灵寺',
        'cuser': cuser,
        'activity_attendees': activity_attendees,
    }
    template = loader.get_template('cuser.html')
    return HttpResponse(template.render(context, request))


@csrf_exempt
def login(request):
    try:
        request.session['cuser_id']
        return HttpResponseRedirect('/cuser/index')
    except Exception, e:
        print e
    error = 0
    if request.method == 'POST':
        phone = request.POST.get('phone', '')
        pwd = request.POST.get('pwd', '')
        try:
            cuser = get_object_or_404(Cuser, phone=phone)
            is_pwd = check_password(pwd, cuser.pwd)
            if is_pwd:
                is_validation = 1
            else:
                is_validation = 0
        except Cuser.DoesNotExist:
            is_validation = 0

        if is_validation:
            request.session['cuser_id'] = cuser.id
            request.session['openid'] = cuser.openid
            # 获取用户ip
            if 'HTTP_X_FORWARDED_FOR' in request.META:
                cuser_ip = request.META['HTTP_X_FORWARDED_FOR']
            else:
                cuser_ip = request.META['REMOTE_ADDR']
            request.session['cuser_ip'] = cuser_ip
            # 其他页登录需要回调
            redirest = request.session.get('redirest', '')
            if redirest:
                return HttpResponseRedirect(redirest)
            return HttpResponseRedirect('/cuser/index')
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
    return HttpResponseRedirect('/cuser/login')


@web_webchat_check_login
def register_do(request):
    if request.method == 'POST':
        phone = request.POST.get('phone', '')
        pwd = request.POST.get('pwd', '')

        cuser, _ = Cuser.objects.get_or_create(openid=request.session.get('openid', ''))
        cuser.phone = phone
        cuser.pwd = make_password(pwd, None, 'pbkdf2_sha256')
        cuser.save()
        # 获取用户ip
        if 'HTTP_X_FORWARDED_FOR' in request.META:
            cuser_ip = request.META['HTTP_X_FORWARDED_FOR']
        else:
            cuser_ip = request.META['REMOTE_ADDR']
        request.session['cuser_ip'] = cuser_ip
        return HttpResponseRedirect('/cuser/index')

    context = {
        'title': '揭西石灵寺',
        'DOMAIN': DOMAIN,
    }
    template = loader.get_template('register.html')
    return HttpResponse(template.render(context, request))


def register(request):
    request.session['register'] = 1
    return HttpResponseRedirect('/cuser/register_do')


@csrf_exempt
def pwd_update(request):
    if request.method == 'POST':
        pwd = request.POST.get('pwd1', '')
        try:
            cuser = get_object_or_404(Cuser, id=request.session['cuser_id'])
            cuser.pwd = make_password(pwd, None, 'pbkdf2_sha256')
            cuser.save()
            return HttpResponseRedirect('/cuser/index')
        except Exception, e:
            return HttpResponseRedirect('/cuser/login')
    context = {
        'title': '揭西石灵寺',
    }
    template = loader.get_template('pwd_update.html')
    return HttpResponse(template.render(context, request))


@web_webchat_check_login
def wx_login(request):
    request.session['register'] = 0
    return HttpResponseRedirect('/cuser/login')


def ch_phone(request, phone):
    cusers = Cuser.objects.filter(phone=phone)
    if cusers:
        return True
    else:
        return False


def check_phone(request, phone):
    cp = ch_phone(request, phone)
    if cp:
        return HttpResponse(simplejson.dumps({'error': 1, 'msg': '该手机号码已注册,请登录'}, ensure_ascii=False))
    else:
        return HttpResponse(simplejson.dumps({'error': 0, 'msg': ''}, ensure_ascii=False))
