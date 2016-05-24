# coding: utf-8

from django.shortcuts import render, get_object_or_404
from django.template import loader
from django.http import HttpResponse, HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Sum
from django.db.models import Count
from ucenter.wx_config import get_wx_config
from ucenter.models import Cuser, Order
from ucenter.wx_auth import web_webchat_check_login
from .models import (
    Temple,
    Mage,
    GoodDeedDay,
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
from settings import UPLOAD_DIR, DOMAIN
import simplejson
import os
import datetime
import time


def index(request):
    temples = Temple.objects.all()
    if temples:
        temple = temples[0]
    else:
        temple = {}
    context = {
        'title': '揭西石灵寺',
        'module': 'shouye',
        'temple': temple,
    }
    template = loader.get_template('shiling/index.html')
    return HttpResponse(template.render(context, request))


def provide_list(request):
    categories = Category.objects.order_by('-id')
    gooddeeddays = GoodDeedDay.objects.all()
    if gooddeeddays:
        gooddeedday = gooddeeddays[0]
    else:
        gooddeedday = {}
    pds = []
    for category in categories:
        provides = Provide.objects.filter(
           category=category,
        ).order_by('-id')
        item = {
            'category': category,
            'provides': provides,
            'pr_is': len(provides) % 2,
        }
        pds.append(item)
    context = {
        'title': '揭西石灵寺',
        'module': 'provide',
        'gooddeedday': gooddeedday,
        'pds': pds,
    }
    template = loader.get_template('shiling/provide.html')
    return HttpResponse(template.render(context, request))


def provide_detail(request, provide_id):
    provide = get_object_or_404(Provide, id=provide_id)
    context = {
        'title': '揭西石灵寺',
        'module': 'provide',
        'provide': provide,
    }
    template = loader.get_template('shiling/provide_detail.html')
    return HttpResponse(template.render(context, request))


@web_webchat_check_login
def provide_pay(request, provide_id):
    cuser_id = request.session.get('cuser_id', 0)
    openid = request.session.get('openid', '')
    if request.method == 'POST':
        if not openid:
            # 设置登录后回调地址
            request.session['redirest'] = request.get_raw_uri()
            return HttpResponseRedirect('/cuser/wx_login')
    provide = get_object_or_404(Provide, id=provide_id)
    context = {
        'wx_config': get_wx_config(request.get_raw_uri()),
        'title': '揭西石灵寺',
        'module': 'provide',
        'provide': provide,
        'cuser_id': cuser_id,
        'openid': openid,
    }
    template = loader.get_template('shiling/provide_pay.html')
    return HttpResponse(template.render(context, request))


def goodraise_list(request):
    cur_time = datetime.datetime.now()
    goodraises = GoodRaise.objects.filter(
        end_time__gte=cur_time,
    )
    for goodraise in goodraises:
        goods = Good.objects.filter(goodraise=goodraise)
        # 统计订单支付成功，总金额
        support_price_num = 0
        for good in goods:
            total_fee_json = Order.objects.filter(good=good, status=2).values('total_fee').annotate(dcount=Count('total_fee'))
            for x in total_fee_json:
                support_price_num = support_price_num + x.get('total_fee')

        goodraise.support_price_num = support_price_num
    context = {
        'title': '揭西石灵寺',
        'module': 'goodraise',
        'goodraises': goodraises,
    }
    template = loader.get_template('shiling/goodraise.html')
    return HttpResponse(template.render(context, request))


def goodraise_detail(request, goodraise_id):
    goodraise = get_object_or_404(GoodRaise, id=goodraise_id)
    goods = Good.objects.filter(goodraise=goodraise)
    support_price_num = 0
    # 统计订单支付成功，总金额
    for good in goods:
        total_fee_json = Order.objects.filter(good=good, status=2).values('total_fee').annotate(dcount=Count('total_fee'))
        for x in total_fee_json:
            support_price_num = support_price_num + x.get('total_fee')

    goodraise.support_price_num = support_price_num
    support_price_num = ret.get('support_price__sum')
    goods = Good.objects.filter(goodraise=goodraise).order_by('-id')
    context = {
        'title': '揭西石灵寺',
        'module': 'goodraise',
        'goodraise': goodraise,
        'support_price_num': support_price_num,
        'goods': goods,
    }
    template = loader.get_template('shiling/goodraise_detail.html')
    return HttpResponse(template.render(context, request))


def good_pay(request, good_id):
    good = get_object_or_404(Good, id=good_id)
    context = {
        'title': '揭西石灵寺',
        'module': 'goodraise',
        'good': good,
    }
    template = loader.get_template('shiling/good_pay.html')
    return HttpResponse(template.render(context, request))


def blessing_list(request):
    temples = Temple.objects.all()
    buddhismknowledge = BuddhismKnowledge.objects.all()
    if temples:
        temple = temples[0]
    else:
        temple = {}
    context = {
        'title': '揭西石灵寺',
        'module': 'blessing',
        'temple': temple,
        'bknow': len(buddhismknowledge),
    }
    template = loader.get_template('shiling/blessing.html')
    return HttpResponse(template.render(context, request))


def activity_list(request):
    cur_time = datetime.datetime.now()
    activitys = Activity.objects.filter(
        end_time__gte=cur_time,
    )
    context = {
        'title': '揭西石灵寺',
        'module': 'activity',
        'activitys': activitys,
    }
    template = loader.get_template('shiling/activity.html')
    return HttpResponse(template.render(context, request))


def activity_detail(request, activity_id):
    activity = get_object_or_404(Activity, id=activity_id)
    activityattendees = ActivityAttendee.objects.filter(
        activity=activity,
    ).order_by('-id')
    context = {
        'title': '揭西石灵寺',
        'module': 'activity',
        'activity': activity,
        'activityattendees': activityattendees,
        'DOMAIN': DOMAIN,
    }
    template = loader.get_template('shiling/activity_detail.html')
    return HttpResponse(template.render(context, request))


@csrf_exempt
def activity_signup(request, activity_id):
    name = request.POST.get('name', '')
    phone = request.POST.get('phone', '')
    activity = get_object_or_404(Activity, id=activity_id)

    activity_attendees1 = ActivityAttendee.objects.filter(
        mobile_phone=phone,
        activity=activity,
    )
    # 义工报名人数
    activity_attendees2 = ActivityAttendee.objects.filter(
        activity=activity,
    )
    if len(activity_attendees1):
        msg_json = {'error': 1, 'msg': '该手机号码已报名'}
    elif len(activity_attendees2) >= activity.people_number:
        msg_json = {'error': 2, 'msg': '报名人数已满'}
    else:
        activityattendee = ActivityAttendee()
        activityattendee.name = name
        activityattendee.mobile_phone = phone
        activityattendee.activity = activity
        activityattendee.save()
        msg_json = {'error': 0, 'msg': '报名成功'}
    return HttpResponse(simplejson.dumps(msg_json, ensure_ascii=False))


def news_list(request):
    cur_time = datetime.datetime.now()
    news = News.objects.filter(
        end_time__gte=cur_time,
    )
    context = {
        'title': '揭西石灵寺',
        'module': 'news',
        'news': news,
    }
    template = loader.get_template('shiling/news.html')
    return HttpResponse(template.render(context, request))


def news_detail(request, news_id):
    new = get_object_or_404(News, id=news_id)
    context = {
        'title': '揭西石灵寺',
        'module': 'news',
        'new': new,
    }
    template = loader.get_template('shiling/news_detail.html')
    return HttpResponse(template.render(context, request))


def volunteer_detail(request):
    cur_time = datetime.datetime.now()
    volunteers = Volunteer.objects.filter(
        end_time__gte=cur_time,
    )
    volunteer = {}
    volunteer_users = {}
    if volunteers:
        volunteer = volunteers[0]
        volunteer_users = VolunteerUser.objects.filter(
            volunteer=volunteer,
        ).order_by('-id')
    context = {
        'title': '揭西石灵寺',
        'module': 'volunteer',
        'volunteer': volunteer,
        'volunteer_users': volunteer_users,
        'DOMAIN': DOMAIN,
    }
    template = loader.get_template('shiling/volunteer.html')
    return HttpResponse(template.render(context, request))


@csrf_exempt
def volunteer_signup(request, volunteer_id):
    name = request.POST.get('name', '')
    phone = request.POST.get('phone', '')
    volunteer = get_object_or_404(Volunteer, id=volunteer_id)

    volunteer_users1 = VolunteerUser.objects.filter(
        mobile_phone=phone,
        volunteer=volunteer,
    )
    # 义工报名人数
    volunteer_users2 = VolunteerUser.objects.filter(
        volunteer=volunteer,
    )
    if len(volunteer_users1):
        msg_json = {'error': 1, 'msg': '该手机号码已报名'}
    elif len(volunteer_users2) >= volunteer.people_number:
        msg_json = {'error': 2, 'msg': '报名人数已满'}
    else:
        volunteeruser = VolunteerUser()
        volunteeruser.name = name
        volunteeruser.mobile_phone = phone
        volunteeruser.volunteer = volunteer
        volunteeruser.save()
        msg_json = {'error': 0, 'msg': '报名成功'}
    return HttpResponse(simplejson.dumps(msg_json, ensure_ascii=False))


def buddhismknowledge_list(request):
    buddhismknowledges = BuddhismKnowledge.objects.all()
    context = {
        'title': '揭西石灵寺',
        'module': 'buddhismknowledge',
        'buddhismknowledges': buddhismknowledges,
    }
    template = loader.get_template('shiling/buddhismknowledge.html')
    return HttpResponse(template.render(context, request))


def buddhismknowledge_detail(request, buddhismknowledge_id):
    buddhismknowledge = get_object_or_404(BuddhismKnowledge, id=buddhismknowledge_id)
    context = {
        'title': '揭西石灵寺',
        'module': 'buddhismknowledge',
        'buddhismknowledge': buddhismknowledge,

    }
    template = loader.get_template('shiling/buddhismknowledge_detail.html')
    return HttpResponse(template.render(context, request))


def host_detail(request, host_id):
    mage = get_object_or_404(Mage, id=host_id)
    context = {
        'title': '主持详情',
        'module': 'shouye',
        'mage': mage,
    }
    template = loader.get_template('shiling/host_detail.html')
    return HttpResponse(template.render(context, request))


def sentiment(request, host_id):
    mage = get_object_or_404(Mage, id=host_id)
    mage.sentiment = mage.sentiment + 1
    mage.save()
    return HttpResponse(simplejson.dumps({'error': 0, 'msg': ''}, ensure_ascii=False))


def views_count(request, activity_id):
    activity = get_object_or_404(Activity, id=activity_id)
    activity.views_count = activity.views_count + 1
    activity.save()
    return HttpResponse(simplejson.dumps({'error': 0, 'msg': ''}, ensure_ascii=False))


def views_count_news(request, news_id):
    news = get_object_or_404(News, id=news_id)
    news.views_count = news.views_count + 1
    news.save()
    return HttpResponse(simplejson.dumps({'error': 0, 'msg': ''}, ensure_ascii=False))


def views_count_volunteer(request, volunteer_id):
    volunteer = get_object_or_404(Volunteer, id=volunteer_id)
    volunteer.views_count = volunteer.views_count + 1
    volunteer.save()
    return HttpResponse(simplejson.dumps({'error': 0, 'msg': ''}, ensure_ascii=False))


def pay_add(request):
    context = {}
    template = loader.get_template('kikkik/login.html')
    return HttpResponse(template.render(context, request))


def upload(request):
    context = {}
    template = loader.get_template('kikkik/login.html')
    return HttpResponse(template.render(context, request))
