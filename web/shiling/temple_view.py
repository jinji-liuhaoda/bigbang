# coding: utf-8

from django.shortcuts import render
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
from settings import UPLOAD_DIR
import os
import datetime
import time


def index(request):
    temple = Temple.objects.get(id=1)
    mage = Mage.objects.get(temple=temple)
    context = {
        'title': '揭西石灵寺',
        'module': 'shouye',
        'temple': temple,
        'mage': mage,
    }
    template = loader.get_template('shiling/index.html')
    return HttpResponse(template.render(context, request))


def provide_list(request):
    # provide = Provide.objects.get(id=1)
    categorys = Category.objects.order_by('-id')
    pds = []
    for category in categorys:
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
    provide = Provide.objects.get(id=provide_id)
    context = {
        'title': '揭西石灵寺',
        'module': 'provide',
        'provide': provide,
    }
    template = loader.get_template('shiling/provide_detail.html')
    return HttpResponse(template.render(context, request))


def goodraise_list(request):
    goodraises = GoodRaise.objects.all()
    context = {
        'title': '揭西石灵寺',
        'module': 'goodraise',
        'goodraises': goodraises,
    }
    template = loader.get_template('shiling/goodraise.html')
    return HttpResponse(template.render(context, request))


def goodraise_detail(request, goodraise_id):
    goodraise = GoodRaise.objects.get(id=goodraise_id)
    goods = Good.objects.filter(goodraise=goodraise).order_by('-id')
    context = {
        'title': '揭西石灵寺',
        'module': 'goodraise',
        'goodraise': goodraise,
        'goods': goods,
    }
    template = loader.get_template('shiling/goodraise_detail.html')
    return HttpResponse(template.render(context, request))


def blessing_list(request):
    temple = Temple.objects.get(id=1)
    mage = Mage.objects.get(temple=temple)
    context = {
        'title': '揭西石灵寺',
        'module': 'blessing',
        'temple': temple,
        'mage': mage,
    }
    template = loader.get_template('shiling/blessing.html')
    return HttpResponse(template.render(context, request))


def activity_list(request):
    activitys = Activity.objects.all()
    context = {
        'title': '揭西石灵寺',
        'module': 'activity',
        'activitys': activitys,
    }
    template = loader.get_template('shiling/activity.html')
    return HttpResponse(template.render(context, request))


def activity_detail(request, activity_id):
    activity = Activity.objects.get(id=activity_id)
    activityattendees = ActivityAttendee.objects.filter(
        activity=activity,
    ).order_by('-id')
    context = {
        'title': '揭西石灵寺',
        'module': 'activity',
        'activity': activity,
        'activityattendees': activityattendees,
    }
    template = loader.get_template('shiling/activity_detail.html')
    return HttpResponse(template.render(context, request))


@csrf_exempt
def activity_signup(request, activity_id):
    if request.method == 'POST':
        name = request.POST.get('name', '')
        phone = request.POST.get('phone', '')
        activity = Activity.objects.get(id=activity_id)

        activityattendee = ActivityAttendee()
        activityattendee.name = name
        activityattendee.mobile_phone = phone
        activityattendee.activity = activity
        activityattendee.save()
    return HttpResponse('报名成功')


def news_list(request):
    news = News.objects.all()
    context = {
        'title': '揭西石灵寺',
        'module': 'news',
        'news': news,
    }
    template = loader.get_template('shiling/news.html')
    return HttpResponse(template.render(context, request))


def news_detail(request, news_id):
    new = News.objects.get(id=news_id)
    context = {
        'title': '揭西石灵寺',
        'module': 'news',
        'new': new,
    }
    template = loader.get_template('shiling/news_detail.html')
    return HttpResponse(template.render(context, request))


def volunteer_detail(request):
    volunteer = Volunteer.objects.get(id=1)
    volunteerusers = VolunteerUser.objects.filter(
        volunteer=volunteer,
    ).order_by('-id')
    context = {
        'title': '揭西石灵寺',
        'module': 'volunteer',
        'volunteer': volunteer,
        'volunteerusers': volunteerusers,
    }
    template = loader.get_template('shiling/volunteer.html')
    return HttpResponse(template.render(context, request))


@csrf_exempt
def volunteer_signup(request, volunteer_id):
    if request.method == 'POST':
        name = request.POST.get('name', '')
        phone = request.POST.get('phone', '')
        volunteer = Volunteer.objects.get(id=volunteer_id)

        volunteeruser = VolunteerUser()
        volunteeruser.name = name
        volunteeruser.mobile_phone = phone
        volunteeruser.volunteer = volunteer
        volunteeruser.save()
    return HttpResponse('报名成功')


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
    buddhismknowledge = BuddhismKnowledge.objects.get(id=buddhismknowledge_id)
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
    mage = Mage.objects.get(id=host_id)
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
