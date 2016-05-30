# coding: utf-8

from django.shortcuts import render, get_object_or_404
from django.template import loader
from django.http import HttpResponse, HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.hashers import make_password, check_password
from attackt.sms import SMSManager
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
from .models import Cuser, Order
from wx_auth import web_webchat_check_login
from settings import UPLOAD_DIR, DOMAIN, SMS_ACCOUNT_SID, SMS_ACCOUNT_TOKEN, SMS_SUB_ACCOUNT_SID, SMS_TEMPLATE_ID, SMS_SUB_ACCOUNT_TOKEN, SMS_APP_ID
import random
import simplejson
import os
import datetime
import time


@csrf_exempt
@web_webchat_check_login
def index(request):
    try:
        cuser = Cuser.objects.get(id=request.session.get('cuser_id', 0))
    except Exception, e:
        return HttpResponseRedirect('/cuser/login')
    cur_time = datetime.datetime.now()
    activity_attendees = ActivityAttendee.objects.filter(mobile_phone=cuser.phone)
    request.session['cuser_id'] = cuser.id
    orders = Order.objects.filter(cuser=cuser, status=2)
    for activity_attendee in activity_attendees:
        if cur_time < activity_attendee.activity.start_time:
            activity_attendee.status_str = '未开启'
        elif cur_time >= activity_attendee.activity.start_time and cur_time <= activity_attendee.activity.end_time:
            activity_attendee.status_str = '开启'
        else:
            activity_attendee.status_str = '已结束'
    context = {
        'title': '揭西石灵寺',
        'cuser': cuser,
        'orders': orders,
        'activity_attendees': activity_attendees,
    }
    template = loader.get_template('cuser.html')
    return HttpResponse(template.render(context, request))


@csrf_exempt
def login(request):
    try:
        cuser = Cuser.objects.get(id=request.session.get('cuser_id', 0))
        return HttpResponseRedirect('/cuser/index')
    except Exception, e:
        request.session.clear()
    context = {
        'title': '揭西石灵寺',
    }
    if request.method == 'POST':
        phone = request.POST.get('phone', '')
        pwd = request.POST.get('pwd', '')
        is_validation = 0

        try:
            cuser = get_object_or_404(Cuser, phone=phone)
            if cuser:
                is_pwd = check_password(pwd, cuser.pwd)
                if is_pwd:
                    is_validation = 1
        except Exception, e:
            print '-----login-error----', phone, pwd

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
            if len(redirest):
                return HttpResponseRedirect(redirest)
            return HttpResponseRedirect('/cuser/index')
        else:
            error = 1
            context['error'] = error

    template = loader.get_template('login.html')
    return HttpResponse(template.render(context, request))


def login_out(request):
    request.session.clear()
    return HttpResponseRedirect('/cuser/login')


@csrf_exempt
@web_webchat_check_login
def register_do(request):
    context = {
        'title': '揭西石灵寺',
        'DOMAIN': DOMAIN,
    }
    if request.method == 'POST':
        phone = request.POST.get('phone', '')
        pwd = request.POST.get('pwd', '')
        v_code = request.POST.get('v_code', '')
        vc_code_json = request.session.get('vc_code_json', '{}')
        vc_code_json = simplejson.loads(vc_code_json)
        if vc_code_json:
            diff_v_time = int(time.time())-int(vc_code_json['send_time'])
        if vc_code_json and (vc_code_json['vc_code'] == v_code) and diff_v_time < 120:
            error_msg = {'error': 0, 'msg': ''}
        elif vc_code_json and (vc_code_json['vc_code'] == v_code) and diff_v_time > 120:
            error_msg = {'error': 1, 'msg': '验证码失效'}
        else:
            error_msg = {'error': 2, 'msg': '验证码错误'}
        context['error_msg'] = simplejson.dumps(error_msg, ensure_ascii=False)
        if not error_msg['error']:
            openid = request.session.get('openid', '')
            name = request.session.get('nickname', '')
            city = request.session.get('city', '')
            province = request.session.get('province', '')
            country = request.session.get('country', '')
            headimgurl = request.session.get('headimgurl', '')
            cuser, _ = Cuser.objects.get_or_create(openid=openid)
            if name:
                cuser.name = name
            if city:
                cuser.city = city
            if province:
                cuser.province = province
            if country:
                cuser.country = country
            if headimgurl:
                cuser.headimgurl = headimgurl
            cuser.phone = phone
            cuser.pwd = make_password(pwd, None, 'pbkdf2_sha256')
            cuser.save()
            # 获取用户ip
            if 'HTTP_X_FORWARDED_FOR' in request.META:
                cuser_ip = request.META['HTTP_X_FORWARDED_FOR']
            else:
                cuser_ip = request.META['REMOTE_ADDR']
            request.session['cuser_ip'] = cuser_ip
            request.session['cuser_id'] = cuser.id
            return HttpResponseRedirect('/cuser/index')
        else:
            context['phone'] = phone
            context['pwd'] = pwd
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
    return HttpResponseRedirect('/cuser/login')


def ch_phone(request, phone):
    cusers = Cuser.objects.filter(phone=phone)
    if cusers:
        return True
    else:
        return False


def send_code(request, phone):
    vc_code = str(random.randint(1000, 9999))
    sms_manager = SMSManager(SMS_ACCOUNT_SID, SMS_ACCOUNT_TOKEN, SMS_SUB_ACCOUNT_SID, SMS_SUB_ACCOUNT_TOKEN, SMS_APP_ID)
    try:
        result = sms_manager.send_auth_code(phone, vc_code, expired_minutes=2, template_id=SMS_TEMPLATE_ID)
        send_status = True
    except Exception, e:
        send_status = False
    if send_status:
        request.session['vc_code_json'] = simplejson.dumps({'vc_code': vc_code, 'send_time': int(time.time())}, ensure_ascii=False)
        return HttpResponse(simplejson.dumps({'error': 0, 'msg': '验证码发送成功'}, ensure_ascii=False))
    else:
        return HttpResponse(simplejson.dumps({'error': 1, 'msg': '验证码发送失败'}, ensure_ascii=False))


def check_phone(request, phone):
    cp = ch_phone(request, phone)
    if cp:
        return HttpResponse(simplejson.dumps({'error': 1, 'msg': '该手机号码已注册,请登录'}, ensure_ascii=False))
    else:
        return HttpResponse(simplejson.dumps({'error': 0, 'msg': ''}, ensure_ascii=False))
