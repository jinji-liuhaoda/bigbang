# coding: utf-8

from django.shortcuts import render, get_object_or_404
from django.template import loader
from django.http import HttpResponse, HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt
from .models import Cuser, Order, GoodId
from wx_auth import web_webchat_check_login

from settings import UPLOAD_DIR, DOMAIN, WX_PAY_MCH_KEY
from .constants import WX_APP_ID, WX_SECRET, WX_MCH_ID
from .wx_config import get_wx_config

import simplejson
import logging
import os
import datetime
import time
import hashlib
import random
import requests
import xml.etree.ElementTree as ET
from xml.sax.saxutils import escape
import sys
reload(sys)
sys.setdefaultencoding("utf-8")


@csrf_exempt
def create_order(request):
    if request.method == 'POST':
        openid = request.session.get('openid', '')
        body = request.POST.get('body', '')
        detail = request.POST.get('detail', '')
        total_fee = request.POST.get('total_fee', '')
        anonymous = request.POST.get('anonymous', '')
        total_fee = str(int(float(total_fee)*100))
        spbill_create_ip = request.session.get('cuser_ip', '')
        out_trade_no = get_out_trade_no()
        product_id = get_product_id()
        noncestr = ''.join(map(lambda xx: (hex(ord(xx))[2:]), os.urandom(8)))
        stringA = "appid=" + WX_APP_ID + "&body=body_str&detail=detail_str&device_info=WEB&mch_id=" + WX_MCH_ID + "&nonce_str=" + noncestr + "&notify_url=" + DOMAIN + "/cuser/wx_pay/&openid=" +openid + "&out_trade_no=" + out_trade_no + "&product_id=" + product_id + "&spbill_create_ip=" + spbill_create_ip + "&total_fee=" + total_fee + "&trade_type=JSAPI"
        stringSignTemp = stringA + "&key=" + WX_PAY_MCH_KEY
        sign = hashlib.md5(stringSignTemp.encode('utf-8')).hexdigest().upper()
        # 生成订单
        order_insert(out_trade_no, product_id, body, detail, total_fee, request, anonymous)
        xml_request = "<xml>\
                           <appid>" + WX_APP_ID + "</appid>\
                           <body>body_str</body>\
                           <detail>detail_str</detail>\
                           <device_info>WEB</device_info>\
                           <mch_id>" + WX_MCH_ID + "</mch_id>\
                           <nonce_str><![CDATA[" + noncestr + "]]></nonce_str>\
                           <notify_url><![CDATA[" + DOMAIN + "/cuser/wx_pay/]]></notify_url>\
                           <openid><![CDATA[" + openid + "]]></openid>\
                           <out_trade_no><![CDATA[" + out_trade_no + "]]></out_trade_no>\
                           <product_id>" + product_id + "</product_id>\
                           <spbill_create_ip><![CDATA[" + spbill_create_ip + "]]></spbill_create_ip>\
                           <total_fee>" + total_fee + "</total_fee>\
                           <trade_type>JSAPI</trade_type>\
                           <sign><![CDATA[" + sign + "]]></sign>\
                        </xml>"
        logging.error(body)
        headers = {'Content-Type': 'application/xml;charset=utf-8;'}
        r = requests.post('https://api.mch.weixin.qq.com/pay/unifiedorder', data=xml_request, headers=headers)
        logging.error(r.text)
        root = ET.fromstring(r.text)
        # 解析xml内容
        for child in root:
            if child.tag == 'return_code':
                return_code = child.text
            if child.tag == 'result_code':
                result_code = child.text
            if child.tag == 'trade_type':
                trade_type = child.text
            if child.tag == 'prepay_id':
                prepay_id = child.text

        if return_code == 'SUCCESS' and result_code == 'SUCCESS':
            # 成功需要修改订单状态
            order = get_object_or_404(Order, out_trade_no=out_trade_no)
            order.trade_type = trade_type
            order.prepay_id = prepay_id
            order.status = 1
            timestamp = str(int(time.time()))
            stringB = "appId=" + WX_APP_ID + "&nonceStr=" + noncestr + "&package=prepay_id=" + prepay_id + "&signType=MD5&timeStamp=" + timestamp
            stringSignTempB = stringB + "&key=" + WX_PAY_MCH_KEY
            signB = hashlib.md5(stringSignTempB.encode('utf-8')).hexdigest().upper()
            wx_pay_json = {'timestamp': timestamp, 'nonceStr': noncestr, 'signType': 'MD5', 'prepay_id': prepay_id, 'paySign': signB}
            return HttpResponse(simplejson.dumps({'error': 0, 'msg': '下单成功', 'wx_pay_json': wx_pay_json}, ensure_ascii=False))
        else:
            return HttpResponse(simplejson.dumps({'error': 1, 'msg': '下单失败'}, ensure_ascii=False))


# 支付成功后微信回调地址
def wx_callback_pay(request):
    if request.method == 'POST':
        prepay_id = request.POST.get('prepay_id', '')
        order = get_object_or_404(Order, id=prepay_id)
        order.status = 2
        order.save()
        return HttpResponse(simplejson.dumps({'error': 0, 'msg': ''}, ensure_ascii=False))


def order_insert(out_trade_no, product_id, body, detail, total_fee, request, anonymous):
    cuser_id = request.session.get('cuser_id', 0)
    order = Order()
    order.cuser = get_object_or_404(Cuser, id=cuser_id)
    order.out_trade_no = out_trade_no
    order.product_id = product_id
    order.body = body
    order.detail = detail
    order.total_fee = total_fee
    order.anonymous = anonymous
    order.status = 0
    order.save()


def get_out_trade_no():
    return str(int(time.time()))+str(random.randint(1000, 9999))


def get_product_id():
    goodid = GoodId()
    goodid.save()
    product_id = goodid.id
    return str(product_id).zfill(8)
