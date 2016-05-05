# coding: utf-8

from django.shortcuts import render
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
from settings import UPLOAD_DIR
import os
import datetime
import time


def index(request, user_id):
    user = User.objects.get(id=user_id)
    activityattendees = ActivityAttendee.objects.filter(mobile_phone=user.phone)
    context = {
        'title': '揭西石灵寺',
        'user': user,
        'activityattendees': activityattendees,
    }
    template = loader.get_template('shiling/user.html')
    return HttpResponse(template.render(context, request))


def login(request):
    error_msg = 0
    if request.method == 'POST':
        phone = request.POST.get('phone', '')
        pwd = request.POST.get('pwd', '')
        try:
            user = User.objects.get(phone=phone)
            user.phone = phone
            is_pwd = check_password(pwd, user.pwd)
            if is_pwd:
                is_t = 1
            else:
                is_t = 0
        except User.DoesNotExist:
            is_t = 0
            if is_t:
                return HttpResponseRedirect('/user/{}'.format(user.id))
            else:
                error_msg = 1
    context = {
        'title': '揭西石灵寺',
        'error_msg': error_msg,
    }
    template = loader.get_template('shiling/login.html')
    return HttpResponse(template.render(context, request))


@csrf_exempt
def register(request):
    if request.method == 'POST':
        phone = request.POST.get('phone', '')
        pwd = request.POST.get('pwd', '')

        user = User()
        user.phone = phone
        user.pwd = make_password(pwd, None, 'pbkdf2_sha256')
        user.save()
        return HttpResponseRedirect('/user/{}'.format(user.id))

    context = {
        'title': '揭西石灵寺',
    }
    template = loader.get_template('shiling/register.html')
    return HttpResponse(template.render(context, request))


@csrf_exempt
def pwdupdate(request, user_id):
    if request.method == 'POST':
        pwd = request.POST.get('pwd1', '')
        u_id = request.POST.get('user_id', '')

        user = User.objects.get(id=u_id)
        user.pwd = make_password(pwd, None, 'pbkdf2_sha256')
        user.save()
        return HttpResponseRedirect('/user/{}'.format(user.id))
    user = User.objects.get(id=user_id)
    context = {
        'title': '揭西石灵寺',
        'user': user,
    }
    template = loader.get_template('shiling/pwdupdate.html')
    return HttpResponse(template.render(context, request))
