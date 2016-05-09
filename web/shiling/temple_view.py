# coding: utf-8

from django.shortcuts import render, get_object_or_404
from django.template import loader
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
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
    temple = Temple.objects.all()[0]
    mage = get_object_or_404(Mage, temple=temple)
    context = {
        'title': '揭西石灵寺',
        'module': 'shouye',
        'temple': temple,
        'mage': mage,
    }
    template = loader.get_template('shiling/index.html')
    return HttpResponse(template.render(context, request))


def provide_list(request):
    categories = Category.objects.order_by('-id')
    pds = []
    for category in categories:
        provides = Provide.objects.filter(
           category=category,
        ).order_by('-id')
        item = {
            'category': category,
            'provides': provides,
            'pr_is': len(provides)%2,
        }
        pds.append(item)
    context = {
        'title': '揭西石灵寺',
        'module': 'provide',
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


def provide_pay(request, provide_id):
    provide = get_object_or_404(Provide, id=provide_id)
    context = {
        'title': '揭西石灵寺',
        'module': 'provide',
        'provide': provide,
    }
    template = loader.get_template('shiling/provide_pay.html')
    return HttpResponse(template.render(context, request))


def goodraise_list(request):
    cur_time = datetime.datetime.now()
    goodraises = GoodRaise.objects.filter(
        end_time__gte=cur_time,
    )
    context = {
        'title': '揭西石灵寺',
        'module': 'goodraise',
        'goodraises': goodraises,
    }
    template = loader.get_template('shiling/goodraise.html')
    return HttpResponse(template.render(context, request))


def goodraise_detail(request, goodraise_id):
    goodraise = get_object_or_404(GoodRaise, id=goodraise_id)
    goods = Good.objects.filter(goodraise=goodraise).order_by('-id')
    context = {
        'title': '揭西石灵寺',
        'module': 'goodraise',
        'goodraise': goodraise,
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
    temple = Temple.objects.all()[0]
    mage = get_object_or_404(Mage, temple=temple)
    context = {
        'title': '揭西石灵寺',
        'module': 'blessing',
        'temple': temple,
        'mage': mage,
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

    ActivityAttendees1 = ActivityAttendee.objects.filter(
        mobile_phone=phone,
        activity=activity,
    )
    #义工报名人数
    ActivityAttendees2 = ActivityAttendee.objects.filter(
        activity=activity,
    )
    if len(ActivityAttendees1) >= 1:
        msg_json = {'error': 1, 'msg': '该手机号码已报名'}
    elif len(ActivityAttendees2) >= activity.people_number:
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
    volunteerusers = {}
    if volunteers:
        volunteer = volunteers[0]
        volunteerusers = VolunteerUser.objects.filter(
            volunteer=volunteer,
        ).order_by('-id')
    context = {
        'title': '揭西石灵寺',
        'module': 'volunteer',
        'volunteer': volunteer,
        'volunteerusers': volunteerusers,
        'DOMAIN': DOMAIN,
    }
    template = loader.get_template('shiling/volunteer.html')
    return HttpResponse(template.render(context, request))


@csrf_exempt
def volunteer_signup(request, volunteer_id):
    name = request.POST.get('name', '')
    phone = request.POST.get('phone', '')
    volunteer = get_object_or_404(Volunteer, id=volunteer_id)

    volunteerusers1 = VolunteerUser.objects.filter(
        mobile_phone=phone,
        volunteer=volunteer,
    )
    #义工报名人数
    volunteerusers2 = VolunteerUser.objects.filter(
        volunteer=volunteer,
    )
    if len(volunteerusers1) >= 1:
        msg_json = {'error': 1, 'msg': '该手机号码已报名'}
    elif len(volunteerusers2) >= volunteer.people_number:
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


def donation_add(request):
    context = {}
    template = loader.get_template('kikkik/login.html')
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


def pay_add(request):
    context = {}
    template = loader.get_template('kikkik/login.html')
    return HttpResponse(template.render(context, request))


def upload(request):
    context = {}
    template = loader.get_template('kikkik/login.html')
    return HttpResponse(template.render(context, request))
