# coding: utf-8

from django.shortcuts import render, get_object_or_404
from django.template import loader
from django.http import HttpResponse, HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.hashers import make_password, check_password
from .models import (
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
    User,
)
from settings import UPLOAD_DIR, DOMAIN
import simplejson
import os
import datetime
import time


def index(request):
    user = get_object_or_404(User, id=request.session['user_id'])
    activity_attendees = ActivityAttendee.objects.filter(mobile_phone=user.phone)
    request.session['user_id'] = user.id
    context = {
        'title': '揭西石灵寺',
        'user': user,
        'activity_attendees': activity_attendees,
    }
    template = loader.get_template('shiling/user.html')
    return HttpResponse(template.render(context, request))


def login(request):
    try:
        request.session['user_id']
        return HttpResponseRedirect('/user/')
    except Exception, e:
        is_login = False
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
            return HttpResponseRedirect('/user/')
        else:
            error = 1
    context = {
        'title': '揭西石灵寺',
        'error': error,
    }
    template = loader.get_template('shiling/login.html')
    return HttpResponse(template.render(context, request))


def login_out(request):
    request.session.flush()
    return HttpResponseRedirect('/login/')


@csrf_exempt
def register(request):
    if request.method == 'POST':
        phone = request.POST.get('phone', '')
        pwd = request.POST.get('pwd', '')

        user = User()
        user.phone = phone
        user.pwd = make_password(pwd, None, 'pbkdf2_sha256')
        user.save()
        request.session['user_id'] = user.id
        return HttpResponseRedirect('/user')

    context = {
        'title': '揭西石灵寺',
        'DOMAIN': DOMAIN,
    }
    template = loader.get_template('shiling/register.html')
    return HttpResponse(template.render(context, request))


@csrf_exempt
def pwd_update(request):
    if request.method == 'POST':
        pwd = request.POST.get('pwd1', '')
        try:
            user = get_object_or_404(User, id=request.session['user_id'])
            user.pwd = make_password(pwd, None, 'pbkdf2_sha256')
            user.save()
            return HttpResponseRedirect('/user/')
        except Exception, e:
            return HttpResponseRedirect('/login')
    context = {
        'title': '揭西石灵寺',
    }
    template = loader.get_template('shiling/pwd_update.html')
    return HttpResponse(template.render(context, request))


def ch_phone(request, phone):
    users = User.objects.filter(phone=phone)
    if len(users) >= 1:
        return True
    else:
        return False


def check_phone(request, phone):
    cp = ch_phone(request, phone)
    if cp:
        return HttpResponse(simplejson.dumps({'error': 1, 'msg': '该手机号码已注册,请登录'}, ensure_ascii = False))
    else:
        return HttpResponse(simplejson.dumps({'error': 0, 'msg': ''}, ensure_ascii=False))
