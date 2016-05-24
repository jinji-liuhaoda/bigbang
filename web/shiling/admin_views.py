# coding: utf-8

from django.shortcuts import render, get_object_or_404
from django.template import loader
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.models import User as DjangoUser
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages
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
from ucenter.models import Order, Cuser
from imagestore.qiniu_manager import upload, url, get_extension, handle_uploaded_file, BUCKET_NAME
from settings import UPLOAD_DIR
import os
import datetime
import time

FILED_CHECK_MSG = '<b class="error_msg">字段为必填项</b>'


def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')
        user = authenticate(username=username, password=password)
        if user is not None and user.is_active:
            login(request, user)
            return HttpResponseRedirect('/admin/')
        else:
            context = {'error': '帐号/密码不正确'}
            template = loader.get_template('manage/login.html')
            return HttpResponse(template.render(context, request))
    context = {}
    template = loader.get_template('manage/login.html')
    return HttpResponse(template.render(context, request))


@login_required
def index(request):
    context = {}
    template = loader.get_template('manage/super/index.html')
    return HttpResponse(template.render(context, request))


@login_required
def logout_view(request):
    logout(request)
    return HttpResponseRedirect('/admin/login')


@login_required
def temple_edit(request):
    temples = Temple.objects.all()
    if temples:
        temple = temples[0]
    else:
        temple = Temple()
    mages = Mage.objects.all()
    error = {}
    if request.method == 'POST':
        flag = True
        name = request.POST.get('name', '')
        title = request.POST.get('title', '')
        detail = request.POST.get('detail', '')
        address = request.POST.get('address', '')
        content = request.POST.get('content', '')
        mage_id = request.POST.get('host_id', '')

        temple.detail = detail
        temple.address = address
        temple.content = content
        if not len(name):
            flag = False
            error['name_msg'] = FILED_CHECK_MSG
        else:
            temple.name = name

        if not len(title):
            flag = False
            error['title_msg'] = FILED_CHECK_MSG
        else:
            temple.title = title
        if not len(mage_id):
            flag = False
            error['mage_id_msg'] = FILED_CHECK_MSG
        else:
            mage = get_object_or_404(Mage, id=mage_id)
            temple.mage = mage
        if flag:
            temple.save()
        if request.FILES:
            if request.FILES.get('cover', None):
                ts = int(time.time())
                ext = get_extension(request.FILES['cover'].name)
                key = 'temple_{}_{}.{}'.format(temple.id, ts, ext)
                handle_uploaded_file(request.FILES['cover'], key)
                temple.cover = key
                temple.save()
                # 上传图片到qiniu
                upload(BUCKET_NAME, key, os.path.join(UPLOAD_DIR, key))

    context = {
        'module': 'temple',
        'temple': temple,
        'mages': mages,
        'error': error,
    }
    if temple:
        context['cover_url'] = temple.cover_url()
    template = loader.get_template('manage/super/temple/edit.html')
    return HttpResponse(template.render(context, request))


@login_required
def mage_list(request):
    temples = Temple.objects.all()
    if temples:
        temple = temples[0]
    else:
        temple = {}
    mages = Mage.objects.all()
    context = {
        'module': 'mage',
        'temple': temple,
        'mages': mages,
    }
    template = loader.get_template('manage/super/mage/list.html')
    return HttpResponse(template.render(context, request))


@login_required
def mage_create(request):
    error = {}
    mage = {}
    if request.method == 'POST':
        flag = True
        name = request.POST.get('name', '')
        mage_num = request.POST.get('mage_num', '')
        detail = request.POST.get('detail', '')
        content = request.POST.get('content', '')

        mage = Mage()
        mage.detail = detail
        mage.content = content
        if not len(name):
            flag = False
            error['name_msg'] = FILED_CHECK_MSG
        else:
            mage.name = name

        if not len(mage_num):
            flag = False
            error['mage_num_msg'] = FILED_CHECK_MSG
        else:
            mage.mage_num = mage_num

        if flag:
            mage.save()
        if request.FILES:
            if request.FILES.get('cover', None):
                ts = int(time.time())
                ext = get_extension(request.FILES['cover'].name)
                key = 'mage_{}_{}.{}'.format(mage.id, ts, ext)
                handle_uploaded_file(request.FILES['cover'], key)
                mage.cover = key
                if flag:
                    mage.save()
                # 上传图片到qiniu
                upload(BUCKET_NAME, key, os.path.join(UPLOAD_DIR, key))
        if flag:
            return HttpResponseRedirect('/admin/mage')
    context = {
        'module': 'mage',
        'error': error,
    }
    if mage:
        context['mage'] = mage
    template = loader.get_template('manage/super/mage/create.html')
    return HttpResponse(template.render(context, request))


@login_required
def mage_edit(request, mage_id):
    mage = get_object_or_404(Mage, id=mage_id)
    error = {}
    if request.method == 'POST':
        flag = True
        name = request.POST.get('name', '')
        mage_num = request.POST.get('mage_num', '')
        detail = request.POST.get('detail', '')
        content = request.POST.get('content', '')
        mage.name = name
        mage.mage_num = mage_num
        mage.detail = detail
        mage.content = content
        if not len(name):
            flag = False
            error['name_msg'] = FILED_CHECK_MSG

        if not len(mage_num):
            flag = False
            error['mage_num_msg'] = FILED_CHECK_MSG

        if flag:
            mage.save()
        if request.FILES:
            if request.FILES.get('cover', None):
                ts = int(time.time())
                ext = get_extension(request.FILES['cover'].name)
                key = 'mage_{}_{}.{}'.format(mage.id, ts, ext)
                handle_uploaded_file(request.FILES['cover'], key)
                mage.cover = key
                if flag:
                    mage.save()
                # 上传图片到qiniu
                upload(BUCKET_NAME, key, os.path.join(UPLOAD_DIR, key))
        if flag:
            return HttpResponseRedirect('/admin/mage')
    context = {
        'module': 'mage',
        'mage': mage,
        'error': error,
    }
    if mage:
        context['cover_url'] = mage.cover_url()
    template = loader.get_template('manage/super/mage/create.html')
    return HttpResponse(template.render(context, request))


@login_required
def mage_delete(request, mage_id):
    kwargs = {
        'id': mage_id,
    }
    mage = get_object_or_404(Mage, **kwargs)
    mage.delete()
    return HttpResponseRedirect("/admin/mage")


@login_required
def gooddeedday_detail(request):
    gooddeeddays = GoodDeedDay.objects.all()
    if gooddeeddays:
        gooddeedday = gooddeeddays[0]
    else:
        gooddeedday = GoodDeedDay()
    error = {}
    if request.method == 'POST':
        flag = True
        title = request.POST.get('title', '')
        sub_title1 = request.POST.get('sub_title1', '')
        sub_detail1 = request.POST.get('sub_detail1', '')
        sub_price1 = request.POST.get('sub_price1', '')
        sub_title2 = request.POST.get('sub_title2', '')
        sub_detail2 = request.POST.get('sub_detail2', '')
        sub_price2 = request.POST.get('sub_price2', '')
        gooddeedday.title = title
        gooddeedday.sub_title1 = sub_title1
        gooddeedday.sub_detail1 = sub_detail1
        gooddeedday.sub_price1 = sub_price1
        gooddeedday.sub_title2 = sub_title2
        gooddeedday.sub_detail2 = sub_detail2
        gooddeedday.sub_price2 = sub_price2
        if not len(title):
            flag = False
            error['title_msg'] = FILED_CHECK_MSG

        if not len(sub_title1):
            flag = False
            error['sub_title1_msg'] = FILED_CHECK_MSG

        if not len(sub_price1):
            flag = False
            error['sub_price1_msg'] = FILED_CHECK_MSG

        if not len(sub_title2):
            flag = False
            error['sub_title2_msg'] = FILED_CHECK_MSG

        if not len(sub_price1):
            flag = False
            error['sub_price2_msg'] = FILED_CHECK_MSG
        if flag:
            gooddeedday.save()
        if request.FILES:
            if request.FILES.get('cover', None):
                ts = int(time.time())
                ext = get_extension(request.FILES['cover'].name)
                key = 'gooddeedday_{}_{}.{}'.format(gooddeedday.id, ts, ext)
                handle_uploaded_file(request.FILES['cover'], key)
                gooddeedday.cover = key
                if flag:
                    gooddeedday.save()
                # 上传图片到qiniu
                upload(BUCKET_NAME, key, os.path.join(UPLOAD_DIR, key))
            if request.FILES.get('sub_cover1', None):
                ts = int(time.time())
                ext = get_extension(request.FILES['sub_cover1'].name)
                key = 'gooddeedday_{}_{}.{}'.format(gooddeedday.id, ts, ext)
                handle_uploaded_file(request.FILES['sub_cover1'], key)
                gooddeedday.sub_cover1 = key
                if flag:
                    gooddeedday.save()
                # 上传图片到qiniu
                upload(BUCKET_NAME, key, os.path.join(UPLOAD_DIR, key))
            if request.FILES.get('sub_cover2', None):
                ts = int(time.time())
                ext = get_extension(request.FILES['sub_cover2'].name)
                key = 'gooddeedday_{}_{}.{}'.format(gooddeedday.id, ts, ext)
                handle_uploaded_file(request.FILES['sub_cover2'], key)
                gooddeedday.sub_cover2 = key
                if flag:
                    gooddeedday.save()
                # 上传图片到qiniu
                upload(BUCKET_NAME, key, os.path.join(UPLOAD_DIR, key))
    context = {
        'module': 'gooddeedday',
        'gooddeedday': gooddeedday,
        'error': error,
    }
    if gooddeedday:
        context['cover_url'] = gooddeedday.cover_url()
        context['sub_cover_url1'] = gooddeedday.sub_cover_url1()
        context['sub_cover_url2'] = gooddeedday.sub_cover_url2()
    template = loader.get_template('manage/super/provide/gooddeedday/edit.html')
    return HttpResponse(template.render(context, request))


@login_required
def category_list(request):
    categorys = Category.objects.all()
    context = {
        'module': 'category',
        'categorys': categorys,
    }
    template = loader.get_template('manage/super/provide/category/list.html')
    return HttpResponse(template.render(context, request))


@login_required
def category_create(request):
    error = {}
    category = {}
    if request.method == 'POST':
        flag = True
        name = request.POST.get('name', '')
        detail = request.POST.get('detail', '')
        category = Category()
        category.name = name
        category.detail = detail
        if not len(name):
            flag = False
            error['name_msg'] = FILED_CHECK_MSG
        if flag:
            category.save()
            return HttpResponseRedirect('/admin/category')
    context = {
        'module': 'category',
        'error': error,
        'category': category,
    }
    template = loader.get_template('manage/super/provide/category/create.html')
    return HttpResponse(template.render(context, request))


@login_required
def category_edit(request, category_id):
    error = {}
    category = get_object_or_404(Category, id=category_id)
    if request.method == 'POST':
        flag = True
        name = request.POST.get('name', '')
        detail = request.POST.get('detail', '')
        category.name = name
        category.detail = detail
        if not len(name):
            flag = False
            error['name_msg'] = FILED_CHECK_MSG
        if flag:
            category.save()
            return HttpResponseRedirect('/admin/category')
    context = {
        'module': 'category',
        'category': category,
        'error': error,
    }
    template = loader.get_template('manage/super/provide/category/create.html')
    return HttpResponse(template.render(context, request))


@login_required
def category_delete(request, category_id):
    kwargs = {
        'id': category_id,
    }
    category = get_object_or_404(Category, **kwargs)
    category.delete()
    return HttpResponseRedirect("/admin/category")


@login_required
def provide_list(request):
    provides = Provide.objects.all()
    context = {
        'module': 'provide',
        'provides': provides,
    }
    template = loader.get_template('manage/super/provide/list.html')
    return HttpResponse(template.render(context, request))


@login_required
def provide_create(request):
    error = {}
    categorys = Category.objects.all()
    provide = {}
    if request.method == 'POST':
        flag = True
        title = request.POST.get('title', '')
        subtitle = request.POST.get('subtitle', '')
        content = request.POST.get('content', '')
        detail = request.POST.get('detail', '')
        price = request.POST.get('price', '')
        category_id = request.POST.get('category_id', '')
        provide = Provide()
        provide.title = title
        provide.subtitle = subtitle
        provide.detail = detail
        provide.content = content
        provide.price = price
        if not len(title):
            flag = False
            error['title_msg'] = FILED_CHECK_MSG

        if not len(subtitle):
            flag = False
            error['subtitle_msg'] = FILED_CHECK_MSG

        if not len(price):
            flag = False
            error['price_msg'] = FILED_CHECK_MSG

        if not len(category_id):
            flag = False
            error['category_id_msg'] = FILED_CHECK_MSG
        if flag:
            category = get_object_or_404(Category, id=category_id)
            provide.category = category
            provide.save()
        if request.FILES:
            if request.FILES.get('cover', None):
                ts = int(time.time())
                ext = get_extension(request.FILES['cover'].name)
                key = 'provide_{}_{}.{}'.format(provide.id, ts, ext)
                handle_uploaded_file(request.FILES['cover'], key)
                provide.cover = key
                if flag:
                    provide.save()
                # 上传图片到qiniu
                upload(BUCKET_NAME, key, os.path.join(UPLOAD_DIR, key))
            if request.FILES.get('banner_cover_url', None):
                ts = int(time.time())
                ext = get_extension(request.FILES['banner_cover_url'].name)
                key = 'provide_banner_{}_{}.{}'.format(provide.id, ts, ext)
                handle_uploaded_file(request.FILES['banner_cover_url'], key)
                provide.banner_cover = key
                if flag:
                    provide.save()
                # 上传图片到qiniu
                upload(BUCKET_NAME, key, os.path.join(UPLOAD_DIR, key))
        if flag:
            return HttpResponseRedirect('/admin/provide')
    context = {
        'module': 'provide',
        'categorys': categorys,
        'provide': provide,
        'error': error,
    }
    template = loader.get_template('manage/super/provide/create.html')
    return HttpResponse(template.render(context, request))


@login_required
def provide_edit(request, provide_id):
    error = {}
    categorys = Category.objects.all()
    provide = get_object_or_404(Provide, id=provide_id)
    if request.method == 'POST':
        flag = True
        title = request.POST.get('title', '')
        subtitle = request.POST.get('subtitle', '')
        content = request.POST.get('content', '')
        detail = request.POST.get('detail', '')
        category_id = request.POST.get('category_id', '')
        price = request.POST.get('price', '')
        provide.title = title
        provide.subtitle = subtitle
        provide.detail = detail
        provide.content = content
        provide.price = price
        if not len(title):
            flag = False
            error['title_msg'] = FILED_CHECK_MSG

        if not len(subtitle):
            flag = False
            error['subtitle_msg'] = FILED_CHECK_MSG

        if not len(price):
            flag = False
            error['price_msg'] = FILED_CHECK_MSG

        if not len(category_id):
            flag = False
            error['category_id_msg'] = FILED_CHECK_MSG
        if flag:
            category = get_object_or_404(Category, id=category_id)
            provide.category = category
            provide.save()
        if request.FILES:
            if request.FILES.get('cover', None):
                ts = int(time.time())
                ext = get_extension(request.FILES['cover'].name)
                key = 'provide_{}_{}.{}'.format(provide.id, ts, ext)
                handle_uploaded_file(request.FILES['cover'], key)
                provide.cover = key
                if flag:
                    provide.save()
                # 上传图片到qiniu
                upload(BUCKET_NAME, key, os.path.join(UPLOAD_DIR, key))
            if request.FILES.get('banner_cover', None):
                ts = int(time.time())
                ext = get_extension(request.FILES['banner_cover'].name)
                key = 'provide_banner_{}_{}.{}'.format(provide.id, ts, ext)
                handle_uploaded_file(request.FILES['banner_cover'], key)
                provide.banner_cover = key
                if flag:
                    provide.save()
                # 上传图片到qiniu
                upload(BUCKET_NAME, key, os.path.join(UPLOAD_DIR, key))
        if flag:
            return HttpResponseRedirect('/admin/provide')
    context = {
        'module': 'provide',
        'provide': provide,
        'categorys': categorys,
        'error': error,
    }
    if provide:
        context['cover_url'] = provide.cover_url()
        context['banner_cover_url'] = provide.banner_cover_url()
    template = loader.get_template('manage/super/provide/create.html')
    return HttpResponse(template.render(context, request))


@login_required
def provide_delete(request, provide_id):
    kwargs = {
        'id': provide_id,
    }
    provide = get_object_or_404(Provide, **kwargs)
    provide.delete()
    return HttpResponseRedirect("/admin/provide")


@login_required
def provide_pay_list(request):
    orders = Order.objects.filter(from_pay=0)
    context = {
        'module': 'provide-pay',
        'orders': orders,
    }
    template = loader.get_template('manage/super/provide-pay/list.html')
    return HttpResponse(template.render(context, request))


@login_required
def good_list(request, goodraise_id):
    goodraise = get_object_or_404(GoodRaise, id=goodraise_id)
    goods = Good.objects.filter(goodraise=goodraise)
    context = {
        'module': 'goodraise',
        'goodraise': goodraise,
        'goods': goods,
    }
    template = loader.get_template('manage/super/good/list.html')
    return HttpResponse(template.render(context, request))


@login_required
def good_create(request, goodraise_id):
    error = {}
    good = {}
    goodraise = get_object_or_404(GoodRaise, id=goodraise_id)
    if request.method == 'POST':
        flag = True
        name = request.POST.get('name', '')
        detail = request.POST.get('detail', '')
        support_price = request.POST.get('support_price', '')
        good = Good()
        good.name = name
        good.detail = detail
        good.goodraise = goodraise
        good.support_price = support_price
        if not len(name):
            flag = False
            error['name_msg'] = FILED_CHECK_MSG
        if not len(support_price):
            flag = False
            error['support_price_msg'] = FILED_CHECK_MSG
        if flag:
            good.save()
            return HttpResponseRedirect('/admin/' + str(goodraise.id) + '/good')
    context = {
        'module': 'goodraise',
        'goodraise': goodraise,
        'good': good,
        'error': error
    }
    template = loader.get_template('manage/super/good/create.html')
    return HttpResponse(template.render(context, request))


@login_required
def good_edit(request, good_id):
    good = get_object_or_404(Good, id=good_id)
    error = {}
    if request.method == 'POST':
        flag = True
        name = request.POST.get('name', '')
        detail = request.POST.get('detail', '')
        support_price = request.POST.get('support_price', '')
        good.name = name
        good.detail = detail
        good.support_price = support_price
        if not len(name):
            flag = False
            error['name_msg'] = FILED_CHECK_MSG
        if not len(support_price):
            flag = False
            error['support_price_msg'] = FILED_CHECK_MSG
        if flag:
            good.save()
            return HttpResponseRedirect('/admin/' + str(good.goodraise.id) + '/good')
    context = {
        'module': 'goodraise',
        'good': good,
        'error': error
    }
    template = loader.get_template('manage/super/good/create.html')
    return HttpResponse(template.render(context, request))


@login_required
def good_delete(request, good_id):
    kwargs = {
        'id': good_id,
    }
    good = get_object_or_404(Good, **kwargs)
    goodraise_id = good.goodraise.id
    good.delete()
    return HttpResponseRedirect("/admin/" + str(goodraise_id) + "/good")


@login_required
def goodraise_list(request):
    goodraises = GoodRaise.objects.all()
    context = {
        'module': 'goodraise',
        'goodraises': goodraises,
    }
    template = loader.get_template('manage/super/goodraise/list.html')
    return HttpResponse(template.render(context, request))


@login_required
def goodraise_create(request):
    error = {}
    goodraise = {}
    if request.method == 'POST':
        flag = True
        title = request.POST.get('title', '')
        total_price = request.POST.get('total_price', '')
        detail = request.POST.get('detail', '')
        content = request.POST.get('content', '')
        daterange = request.POST.get('daterange', '')

        arr = [r.strip() for r in daterange.split('-')]

        try:
            start_time = datetime.datetime.strptime(arr[0], '%m/%d/%Y').date()
            end_time = datetime.datetime.strptime(arr[1], '%m/%d/%Y').date()
        except Exception, e:
            daterange = False
        goodraise = GoodRaise()
        goodraise.title = title
        goodraise.total_price = total_price
        goodraise.detail = detail
        goodraise.content = content
        if not len(title):
            flag = False
            error['title_msg'] = FILED_CHECK_MSG

        if not len(total_price):
            flag = False
            error['total_price_msg'] = FILED_CHECK_MSG

        if not daterange:
            flag = False
            error['daterange_msg'] = FILED_CHECK_MSG
        else:
            goodraise.start_time = start_time
            goodraise.end_time = end_time
        if flag:
            goodraise.save()
        if request.FILES:
            if request.FILES.get('cover', None):
                ts = int(time.time())
                ext = get_extension(request.FILES['cover'].name)
                key = 'goodraise_{}_{}.{}'.format(goodraise.id, ts, ext)
                handle_uploaded_file(request.FILES['cover'], key)
                goodraise.cover = key
                if flag:
                    goodraise.save()
                # 上传图片到qiniu
                upload(BUCKET_NAME, key, os.path.join(UPLOAD_DIR, key))
        if flag:
            return HttpResponseRedirect('/admin/goodraise')
    context = {
        'module': 'goodraise',
        'goodraise': goodraise,
        'error': error
    }
    template = loader.get_template('manage/super/goodraise/create.html')
    return HttpResponse(template.render(context, request))


@login_required
def goodraise_edit(request, goodraise_id):
    error = {}
    goodraise = get_object_or_404(GoodRaise, id=goodraise_id)
    if request.method == 'POST':
        flag = True
        title = request.POST.get('title', '')
        daterange = request.POST.get('daterange', '')
        total_price = request.POST.get('total_price', '')
        detail = request.POST.get('detail', '')
        content = request.POST.get('content', '')

        arr = [r.strip() for r in daterange.split('-')]

        try:
            start_time = datetime.datetime.strptime(arr[0], '%m/%d/%Y').date()
            end_time = datetime.datetime.strptime(arr[1], '%m/%d/%Y').date()
        except Exception, e:
            daterange = False

        goodraise.title = title
        goodraise.total_price = total_price
        goodraise.detail = detail
        if not len(title):
            flag = False
            error['title_msg'] = FILED_CHECK_MSG

        if not len(total_price):
            flag = False
            error['total_price_msg'] = FILED_CHECK_MSG

        if not daterange:
            flag = False
            error['daterange_msg'] = FILED_CHECK_MSG
        else:
            goodraise.start_time = start_time
            goodraise.end_time = end_time
        if flag:
            goodraise.save()
        if request.FILES:
            if request.FILES.get('cover', None):
                ts = int(time.time())
                ext = get_extension(request.FILES['cover'].name)
                key = 'goodraise_{}_{}.{}'.format(goodraise.id, ts, ext)
                handle_uploaded_file(request.FILES['cover'], key)
                goodraise.cover = key
                if flag:
                    goodraise.save()
                # 上传图片到qiniu
                upload(BUCKET_NAME, key, os.path.join(UPLOAD_DIR, key))
        if flag:
            return HttpResponseRedirect('/admin/goodraise')
    context = {
        'module': 'goodraise',
        'goodraise': goodraise,
        'error': error
    }
    if goodraise:
        context['cover_url'] = goodraise.cover_url()
    template = loader.get_template('manage/super/goodraise/create.html')
    return HttpResponse(template.render(context, request))


@login_required
def goodraise_delete(request, goodraise_id):
    kwargs = {
        'id': goodraise_id,
    }
    goodraise = get_object_or_404(GoodRaise, **kwargs)
    goodraise.delete()
    return HttpResponseRedirect("/admin/goodraise")


@login_required
def goodraise_pay_list(request):
    orders = Order.objects.filter(from_pay=1)
    context = {
        'module': 'goodraise-pay',
        'orders': orders,
    }
    template = loader.get_template('manage/super/goodraise-pay/list.html')
    return HttpResponse(template.render(context, request))


@login_required
def activity_list(request):
    activitys = Activity.objects.all()
    context = {
        'module': 'activity',
        'activitys': activitys,
    }
    template = loader.get_template('manage/super/activity/list.html')
    return HttpResponse(template.render(context, request))


@login_required
def activity_create(request):
    error = {}
    activity = {}
    if request.method == 'POST':
        flag = True
        name = request.POST.get('name', '')
        title = request.POST.get('title', '')
        detail = request.POST.get('detail', '')
        content = request.POST.get('content', '')
        address = request.POST.get('address', '')
        people_number = request.POST.get('people_number', '')
        daterange = request.POST.get('daterange', '')

        arr = [r.strip() for r in daterange.split('-')]

        try:
            start_time = datetime.datetime.strptime(arr[0], '%m/%d/%Y').date()
            end_time = datetime.datetime.strptime(arr[1], '%m/%d/%Y').date()
        except Exception, e:
            daterange = False

        activity = Activity()
        activity.name = name
        activity.title = title
        activity.detail = detail
        activity.content = content
        activity.address = address
        activity.people_number = people_number
        if not len(name):
            flag = False
            error['name_msg'] = FILED_CHECK_MSG
        if not len(title):
            flag = False
            error['title_msg'] = FILED_CHECK_MSG
        if not len(people_number):
            flag = False
            error['people_number_msg'] = FILED_CHECK_MSG
        if not daterange:
            flag = False
            error['daterange_msg'] = FILED_CHECK_MSG
        else:
            activity.start_time = start_time
            activity.end_time = end_time
        if flag:
            activity.save()
        if request.FILES:
            if request.FILES.get('cover', None):
                ts = int(time.time())
                ext = get_extension(request.FILES['cover'].name)
                key = 'activity_{}_{}.{}'.format(activity.id, ts, ext)
                handle_uploaded_file(request.FILES['cover'], key)
                activity.cover = key
                if flag:
                    activity.save()
                # 上传图片到qiniu
                upload(BUCKET_NAME, key, os.path.join(UPLOAD_DIR, key))
        if flag:
            return HttpResponseRedirect('/admin/activity')
    context = {
        'module': 'activity',
        'activity': activity,
        'error': error,
    }
    template = loader.get_template('manage/super/activity/create.html')
    return HttpResponse(template.render(context, request))


@login_required
def activity_edit(request, activity_id):
    error = {}
    activity = get_object_or_404(Activity, id=activity_id)
    if request.method == 'POST':
        flag = True
        name = request.POST.get('name', '')
        title = request.POST.get('title', '')
        detail = request.POST.get('detail', '')
        content = request.POST.get('content', '')
        address = request.POST.get('address', '')
        people_number = request.POST.get('people_number', '')
        daterange = request.POST.get('daterange', '')

        arr = [r.strip() for r in daterange.split('-')]

        try:
            start_time = datetime.datetime.strptime(arr[0], '%m/%d/%Y').date()
            end_time = datetime.datetime.strptime(arr[1], '%m/%d/%Y').date()
        except Exception, e:
            daterange = False

        activity.name = name
        activity.title = title
        activity.detail = detail
        activity.content = content
        activity.address = address
        activity.people_number = people_number
        activity.start_time = start_time
        activity.end_time = end_time
        if not len(name):
            flag = False
            error['name_msg'] = FILED_CHECK_MSG
        if not len(title):
            flag = False
            error['title_msg'] = FILED_CHECK_MSG
        if not len(people_number):
            flag = False
            error['people_number_msg'] = FILED_CHECK_MSG
        if not daterange:
            flag = False
            error['daterange_msg'] = FILED_CHECK_MSG
        else:
            activity.start_time = start_time
            activity.end_time = end_time
        if flag:
            activity.save()
        if request.FILES:
            if request.FILES.get('cover', None):
                ts = int(time.time())
                ext = get_extension(request.FILES['cover'].name)
                key = 'activity_{}_{}.{}'.format(activity.id, ts, ext)
                handle_uploaded_file(request.FILES['cover'], key)
                activity.cover = key
                if flag:
                    activity.save()
                # 上传图片到qiniu
                upload(BUCKET_NAME, key, os.path.join(UPLOAD_DIR, key))
        if flag:
            return HttpResponseRedirect('/admin/activity')
    context = {
        'module': 'activity',
        'activity': activity,
        'error': error,
    }
    if activity:
        context['cover_url'] = activity.cover_url()
    template = loader.get_template('manage/super/activity/create.html')
    return HttpResponse(template.render(context, request))


@login_required
def activity_delete(request, activity_id):
    kwargs = {
        'id': activity_id,
    }
    activity = get_object_or_404(Activity, **kwargs)
    activity.delete()
    return HttpResponseRedirect("/admin/activity")


@login_required
def activity_attendee_list(request, activity_id):
    activity = get_object_or_404(Activity, id=activity_id)
    activityattendees = ActivityAttendee.objects.filter(activity=activity)
    context = {
        'module': 'activity',
        'activityattendees': activityattendees,
    }
    template = loader.get_template('manage/super/activity/activityattendee/list.html')
    return HttpResponse(template.render(context, request))


@login_required
def activityattendee_edit(request, activityattendee_id):
    activityattendee = get_object_or_404(ActivityAttendee, id=activityattendee_id)
    if request.method == 'POST':
        name = request.POST.get('name', '')
        mobile_phone = request.POST.get('mobile_phone', '')

        activityattendee.name = name
        activityattendee.mobile_phone = mobile_phone
        activityattendee.save()

        return HttpResponseRedirect('/admin/' + str(activityattendee.activity.id) + '/activityattendee')
    context = {
        'module': 'activity',
        'activityattendee': activityattendee,
    }
    template = loader.get_template('manage/super/activity/activityattendee/create.html')
    return HttpResponse(template.render(context, request))


@login_required
def activityattendee_delete(request, activityattendee_id):
    kwargs = {
        'id': activityattendee_id,
    }
    activityattendee = get_object_or_404(ActivityAttendee, **kwargs)
    activity_id = activityattendee.activity.id
    activityattendee.delete()
    return HttpResponseRedirect("/admin/" + str(activity_id) + "/activityattendee")


@login_required
def news_list(request):
    newss = News.objects.all()
    context = {
        'module': 'news',
        'newss': newss,
    }
    template = loader.get_template('manage/super/news/list.html')
    return HttpResponse(template.render(context, request))


@login_required
def news_create(request):
    error = {}
    news = {}
    if request.method == 'POST':
        flag = True
        title = request.POST.get('title', '')
        detail = request.POST.get('detail', '')
        content = request.POST.get('content', '')
        daterange = request.POST.get('daterange', '')

        arr = [r.strip() for r in daterange.split('-')]

        try:
            start_time = datetime.datetime.strptime(arr[0], '%m/%d/%Y').date()
            end_time = datetime.datetime.strptime(arr[1], '%m/%d/%Y').date()
        except Exception, e:
            daterange = False

        news = News()
        news.title = title
        news.detail = detail
        news.content = content
        if not len(title):
            flag = False
            error['title_msg'] = FILED_CHECK_MSG
        if not daterange:
            flag = False
            error['daterange_msg'] = FILED_CHECK_MSG
        else:
            news.start_time = start_time
            news.end_time = end_time
        if flag:
            news.save()
        if request.FILES:
            if request.FILES.get('cover', None):
                ts = int(time.time())
                ext = get_extension(request.FILES['cover'].name)
                key = 'news_{}_{}.{}'.format(news.id, ts, ext)
                handle_uploaded_file(request.FILES['cover'], key)
                news.cover = key
                if flag:
                    news.save()
                # 上传图片到qiniu
                upload(BUCKET_NAME, key, os.path.join(UPLOAD_DIR, key))
        if flag:
            return HttpResponseRedirect('/admin/news')
    context = {
        'module': 'news',
        'error': error,
        'news': news,
    }
    template = loader.get_template('manage/super/news/create.html')
    return HttpResponse(template.render(context, request))


@login_required
def news_edit(request, news_id):
    error = {}
    news = get_object_or_404(News, id=news_id)
    if request.method == 'POST':
        flag = True
        title = request.POST.get('title', '')
        detail = request.POST.get('detail', '')
        content = request.POST.get('content', '')
        daterange = request.POST.get('daterange', '')

        arr = [r.strip() for r in daterange.split('-')]

        try:
            start_time = datetime.datetime.strptime(arr[0], '%m/%d/%Y').date()
            end_time = datetime.datetime.strptime(arr[1], '%m/%d/%Y').date()
        except Exception, e:
            daterange = False

        news.title = title
        news.detail = detail
        news.content = content
        if not len(title):
            flag = False
            error['title_msg'] = FILED_CHECK_MSG
        if not daterange:
            flag = False
            error['daterange_msg'] = FILED_CHECK_MSG
        else:
            news.start_time = start_time
            news.end_time = end_time
        if flag:
            news.save()
        if request.FILES:
            if request.FILES.get('cover', None):
                ts = int(time.time())
                ext = get_extension(request.FILES['cover'].name)
                key = 'news_{}_{}.{}'.format(news.id, ts, ext)
                handle_uploaded_file(request.FILES['cover'], key)
                news.cover = key
                if flag:
                    news.save()
                # 上传图片到qiniu
                upload(BUCKET_NAME, key, os.path.join(UPLOAD_DIR, key))
        if flag:
            return HttpResponseRedirect('/admin/news')
    context = {
        'module': 'news',
        'news': news,
        'error': error,
    }
    if news:
        context['cover_url'] = news.cover_url()
    template = loader.get_template('manage/super/news/create.html')
    return HttpResponse(template.render(context, request))


@login_required
def news_delete(request, news_id):
    kwargs = {
        'id': news_id,
    }
    news = get_object_or_404(News, **kwargs)
    news.delete()
    return HttpResponseRedirect("/admin/news")


@login_required
def volunteer_detail(request):
    volunteers = Volunteer.objects.all()
    if volunteers:
        volunteer = volunteers[0]
    else:
        volunteer = Volunteer()
    error = {}
    if request.method == 'POST':
        flag = True
        title = request.POST.get('title', '')
        address = request.POST.get('address', '')
        people_number = request.POST.get('people_number', '')
        detail = request.POST.get('detail', '')
        content = request.POST.get('content', '')
        daterange = request.POST.get('daterange', '')
        arr = [r.strip() for r in daterange.split('-')]

        try:
            start_time = datetime.datetime.strptime(arr[0], '%m/%d/%Y').date()
            end_time = datetime.datetime.strptime(arr[1], '%m/%d/%Y').date()
        except Exception, e:
            daterange = False

        volunteer.title = title
        volunteer.address = address
        volunteer.people_number = people_number
        volunteer.detail = detail
        volunteer.content = content
        if not len(title):
            flag = False
            error['title_msg'] = FILED_CHECK_MSG
        if not len(people_number):
            flag = False
            error['people_number_msg'] = FILED_CHECK_MSG
        if not daterange:
            flag = False
            error['daterange_msg'] = FILED_CHECK_MSG
        else:
            volunteer.start_time = start_time
            volunteer.end_time = end_time
        if flag:
            volunteer.save()
        if request.FILES:
            if request.FILES.get('cover', None):
                ts = int(time.time())
                ext = get_extension(request.FILES['cover'].name)
                key = 'volunteer_{}_{}.{}'.format(volunteer.id, ts, ext)
                handle_uploaded_file(request.FILES['cover'], key)
                volunteer.cover = key
                if flag:
                    volunteer.save()
                # 上传图片到qiniu
                upload(BUCKET_NAME, key, os.path.join(UPLOAD_DIR, key))
    context = {
        'module': 'volunteer',
        'volunteer': volunteer,
        'error': error,
    }
    if volunteer:
        context['cover_url'] = volunteer.cover_url()
    template = loader.get_template('manage/super/volunteer/edit.html')
    return HttpResponse(template.render(context, request))


@login_required
def volunteeruser_list(request, volunteer_id):
    volunteer = get_object_or_404(Volunteer, id=volunteer_id)
    volunteerusers = VolunteerUser.objects.filter(volunteer=volunteer)
    context = {
        'module': 'volunteer',
        'volunteerusers': volunteerusers,
    }
    template = loader.get_template('manage/super/volunteer/volunteeruser/list.html')
    return HttpResponse(template.render(context, request))


@login_required
def volunteeruser_edit(request, volunteeruser_id):
    volunteeruser = get_object_or_404(VolunteerUser, id=volunteeruser_id)
    if request.method == 'POST':
        name = request.POST.get('name', '')
        mobile_phone = request.POST.get('mobile_phone', '')

        volunteeruser.name = name
        volunteeruser.mobile_phone = mobile_phone
        volunteeruser.save()

        return HttpResponseRedirect('/admin/' + str(volunteeruser.volunteer.id) + '/volunteeruser')
    context = {
        'module': 'volunteer',
        'volunteeruser': volunteeruser,
    }
    template = loader.get_template('manage/super/volunteer/volunteeruser/create.html')
    return HttpResponse(template.render(context, request))


@login_required
def volunteeruser_delete(request, volunteeruser_id):
    kwargs = {
        'id': volunteeruser_id,
    }
    volunteeruser = get_object_or_404(VolunteerUser, **kwargs)
    volunteer_id = volunteeruser.volunteer.id
    volunteeruser.delete()
    return HttpResponseRedirect("/admin/" + str(volunteer_id) + "/volunteeruser")


@login_required
def buddhismknowledge_list(request):
    buddhismknowledges = BuddhismKnowledge.objects.all()
    context = {
        'module': 'buddhismknowledge',
        'buddhismknowledges': buddhismknowledges,
    }
    template = loader.get_template('manage/super/buddhismknowledge/list.html')
    return HttpResponse(template.render(context, request))


@login_required
def buddhismknowledge_create(request):
    error = {}
    buddhismknowledge = {}
    if request.method == 'POST':
        flag = True
        title = request.POST.get('title', '')
        subtitle = request.POST.get('subtitle', '')
        content = request.POST.get('content', '')

        buddhismknowledge = BuddhismKnowledge()
        buddhismknowledge.title = title
        buddhismknowledge.subtitle = subtitle
        buddhismknowledge.content = content
        if not len(title):
            flag = False
            error['title_msg'] = FILED_CHECK_MSG
        if not len(subtitle):
            flag = False
            error['subtitle_msg'] = FILED_CHECK_MSG
        if flag:
            buddhismknowledge.save()
        if request.FILES:
            if request.FILES.get('cover', None):
                ts = int(time.time())
                ext = get_extension(request.FILES['cover'].name)
                key = 'news_{}_{}.{}'.format(buddhismknowledge.id, ts, ext)
                handle_uploaded_file(request.FILES['cover'], key)
                buddhismknowledge.cover = key
                if flag:
                    buddhismknowledge.save()
                # 上传图片到qiniu
                upload(BUCKET_NAME, key, os.path.join(UPLOAD_DIR, key))
        if flag:
            return HttpResponseRedirect('/admin/buddhismknowledge')
    context = {
        'module': 'buddhismknowledge',
        'buddhismknowledge': buddhismknowledge,
        'error': error,
    }
    template = loader.get_template('manage/super/buddhismknowledge/create.html')
    return HttpResponse(template.render(context, request))


@login_required
def buddhismknowledge_edit(request, buddhismknowledge_id):
    error = {}
    buddhismknowledge = get_object_or_404(BuddhismKnowledge, id=buddhismknowledge_id)
    if request.method == 'POST':
        flag = True
        title = request.POST.get('title', '')
        subtitle = request.POST.get('subtitle', '')
        content = request.POST.get('content', '')

        buddhismknowledge.title = title
        buddhismknowledge.subtitle = subtitle
        buddhismknowledge.content = content
        if not len(title):
            flag = False
            error['title_msg'] = FILED_CHECK_MSG
        if not len(subtitle):
            flag = False
            error['subtitle_msg'] = FILED_CHECK_MSG
        if flag:
            buddhismknowledge.save()
        if request.FILES:
            if request.FILES.get('cover', None):
                ts = int(time.time())
                ext = get_extension(request.FILES['cover'].name)
                key = 'news_{}_{}.{}'.format(buddhismknowledge.id, ts, ext)
                handle_uploaded_file(request.FILES['cover'], key)
                buddhismknowledge.cover = key
                if flag:
                    buddhismknowledge.save()
                # 上传图片到qiniu
                upload(BUCKET_NAME, key, os.path.join(UPLOAD_DIR, key))
        if flag:
            return HttpResponseRedirect('/admin/buddhismknowledge')
    context = {
        'module': 'buddhismknowledge',
        'buddhismknowledge': buddhismknowledge,
        'error': error,
    }
    if buddhismknowledge:
        context['cover_url'] = buddhismknowledge.cover_url()
    template = loader.get_template('manage/super/buddhismknowledge/create.html')
    return HttpResponse(template.render(context, request))


@login_required
def buddhismknowledge_delete(request, buddhismknowledge_id):
    kwargs = {
        'id': buddhismknowledge_id,
    }
    buddhismknowledge = get_object_or_404(BuddhismKnowledge, **kwargs)
    buddhismknowledge.delete()
    return HttpResponseRedirect("/admin/buddhismknowledge")


@login_required
def cuser_list(request):
    cusers = Cuser.objects.all()
    context = {
        'module': 'cuser',
        'cusers': cusers,
    }
    template = loader.get_template('manage/super/cuser/list.html')
    return HttpResponse(template.render(context, request))


@login_required
def cuser_create(request):
    if request.method == 'POST':
        name = request.POST.get('name', '')
        city = request.POST.get('city', '')

        cuser = Cuser()
        cuser.name = name
        cuser.city = city
        if len(cuser.name):
            cuser.save()
        return HttpResponseRedirect('/admin/cuser')
    context = {
        'module': 'cuser',
    }
    template = loader.get_template('manage/super/cuser/create.html')
    return HttpResponse(template.render(context, request))


@login_required
def cuser_edit(request, cuser_id):
    cuser = get_object_or_404(Cuser, id=cuser_id)
    if request.method == 'POST':
        name = request.POST.get('name', '')
        city = request.POST.get('city', '')

        cuser.name = name
        cuser.city = city
        if len(cuser.name):
            cuser.save()
        return HttpResponseRedirect('/admin/cuser')
    context = {
        'module': 'cuser',
        'cuser': cuser,
    }
    template = loader.get_template('manage/super/cuser/create.html')
    return HttpResponse(template.render(context, request))


@login_required
def cuser_delete(request, cuser_id):
    kwargs = {
        'id': cuser_id,
    }
    cuser = get_object_or_404(Cuser, **kwargs)
    cuser.delete()
    return HttpResponseRedirect("/admin/cuser")


@login_required
def user_list(request):
    users = DjangoUser.objects.all()
    context = {
        'module': 'user',
        'users': users,
    }
    template = loader.get_template('manage/super/user/list.html')
    return HttpResponse(template.render(context, request))


@login_required
def user_create(request):
    if request.method == 'POST':
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')

        if not username or not password:
            messages.add_message(request, messages.ERROR, '用户名密码不能为空')
            return HttpResponseRedirect('/admin/user/create')

        try:
            user = DjangoUser.objects.create_user(username, password=password)
        except Exception, e:
            messages.add_message(request, messages.ERROR, '该用户名已经存在, 请换一个用户名试试')
            return HttpResponseRedirect('/admin/user/create')
        return HttpResponseRedirect('/admin/user')
    context = {
        'module': 'user',
    }
    template = loader.get_template('manage/super/user/create.html')
    return HttpResponse(template.render(context, request))


@login_required
def user_edit(request, user_id):
    user = get_object_or_404(DjangoUser, id=user_id)
    if request.method == 'POST':
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')
        user.username = username
        if password:
            user.set_password(password)
        try:
            user.save()
        except:
            return HttpResponseRedirect("/admin/" + str(user.id) + "edit")
        return HttpResponseRedirect("/admin/user")
    context = {
        'module': 'user',
        'nuser': user,
    }
    template = loader.get_template('manage/super/user/create.html')
    return HttpResponse(template.render(context, request))


@login_required
def user_delete(request, user_id):
    kwargs = {
        'id': user_id,
    }
    user = get_object_or_404(DjangoUser, **kwargs)
    user.delete()
    return HttpResponseRedirect("/admin/user")


@csrf_exempt
def ckeditor_upload(request):
    temples = Temple.objects.all()
    if temples:
        temple = temples[0]
    else:
        temple = {}
    if request.FILES:
        ts = int(time.time())
        checkNum = request.GET.get('CKEditorFuncNum')
        ext = get_extension(request.FILES['upload'].name)
        key = 'temple_{}.{}'.format(ts, ext)
        handle_uploaded_file(request.FILES['upload'], key)
        # 上传图片到qiniu
        upload(BUCKET_NAME, key, os.path.join(UPLOAD_DIR, key))
        return HttpResponse("<script type='text/javascript'>window.parent.CKEDITOR.tools.callFunction(\
            '"+checkNum+"','"+url(BUCKET_NAME, key)+"','')</script>")
