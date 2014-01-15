# -*- coding:utf-8 -*-
from django.core import serializers
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render_to_response
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
import httplib
from threading import Thread
import urllib
import uuid

from alipay_python.accounts.models import Buyer
from alipay_python.alipay.alipay import *
from models import Bill, Notify


logger1 = logging.getLogger(__name__)
logger1.setLevel(logging.INFO)
logger1.addHandler(logging.FileHandler(LOGGING_PAYMENT))

_TYPE_ALIPAY = 0

@csrf_exempt
def notify_url_handler(request):
    """
    Handler for notify_url for asynchronous updating billing information.
    Logging the information.
    """
    if request.method == 'POST':
        logger1.info('get post')
        logger1.info(request.POST)
        if notify_verify(request.POST):
            logger1.info('verify ok')
            # save the bill
            bill = Bill(out_trade_no=request.POST.get('out_trade_no'),
                        in_trade_no=gen_inner_trade_no(_TYPE_ALIPAY),  # inner trade number
                        subject=request.POST.get('subject'),
                        type=request.POST.get('type'),
                        trade_no=request.POST.get('trade_no'),
                        trade_status=request.POST.get('trade_status'),
                        seller_id=request.POST.get('seller_id'),
                        seller_email=request.POST.get('seller_email'),
                        buyer_id=request.POST.get('buyer_id'),
                        buyer_email=request.POST.get('buyer_email'),
                        total_fee=request.POST.get('total_fee'),
                        quantity=request.POST.get('quantity'),
                        price=request.POST.get('price'),
                        body=request.POST.get('body'),
                        gmt_create=request.POST.get('gmt_create'),
                        gmt_payment=request.POST.get('gmt_payment'),
                        is_total_fee_adjust=request.POST.get('is_total_fee_adjust'),
                        use_coupon=request.POST.get('use_coupon'),
                        discount=request.POST.get('discount'))
            bill.save()
            logger1.info('save bill')
            logger1.info(bill.as_list())

            # save the user
            users = Buyer.objects.filter(buyer_id=request.POST.get('buyer_id'))
            if not users:
                users = Buyer(name='',
                              buyer_id=bill.buyer_id,
                              buyer_email=bill.buyer_email)
                users.save()
                logger1.info('save user')
                logger1.info(users.as_list())

            # save this notify
            notify = Notify(time=request.POST.get('notify_time'),
                            type=request.POST.get('notify_type'),
                            nid=request.POST.get('notify_id'),
                            sign_type=request.POST.get('sign_type'),
                            sign=request.POST.get('sign'),
                            bill=bill)
            notify.save()
            logger1.info('save notify')
            logger1.info(notify.as_list())

            # start new thread to notify partner
            appid = bill.get_appid()
            logger1.info('appid: ' + appid)
            partner = Partner.objects.get(app_id=appid)
            if partner.real != 1:
                return HttpResponse("fail")
            params = {'out_trade_no':str(bill.out_trade_no)[len(partner.app_id) - 1:],
                      'subject': str(bill.subject),
                      'buyer_id': str(bill.buyer_id),
                      'buyer_email': str(bill.buyer_email),
                      'fee': str(bill.total_fee),
                      'sign_type': 'MD5'}
            _, paramstr = params_filter(params)
            sign = build_mysign(paramstr, partner.app_key)
            params.update({'sign': sign, })
            if partner:
                thread = Thread(target=notify_partner, args=(bill, partner.get_doamin(), partner.get_url(), params))
                thread.start()

            return HttpResponse('success')
    return HttpResponse("fail")

def gen_inner_trade_no(pay_type):
    gen_id = str(uuid.uuid4()).replace('-', '')
    if pay_type == _TYPE_ALIPAY:
        gen_id = 'ap' + gen_id
    return gen_id

def return_url_handler(request):
    """
    Handler for synchronous updating billing information.
    """
    if notify_verify(request.GET):
        tn = request.GET.get('out_trade_no')
        trade_no = request.GET.get('trade_no')
        bill = Bill.objects.get(pk=tn)
        return HttpResponseRedirect(reverse('payment_success'))
    return HttpResponseRedirect(reverse('payment_error'))


def check_url_handle(request):
    if notify_verify(request.POST):
        bill = Bill.objects.get(out_trade_no=request.POST.get('out_trade_no'))
        if bill:
            return HttpResponse('true')
        else:
            return HttpResponse('false')
    return HttpResponse('false')


def index(request):
    return HttpResponse('home')


# notify partern's handler page
def notify_partner(bill, domain, url, params):
    con = httplib.HTTPConnection(domain)
    param = urllib.urlencode(params)
    headers = {"Content-type": "application/x-www-form-urlencoded", "Accept": "text/plain"}
    logger1.info(param)
    con.request('POST', '/' + url, param, headers)
    resp = con.getresponse()
    logger1.info(resp.read())
    if resp.read() == 'success':
        bill.trade_status = 'OK'
        bill.save()

@csrf_exempt
@require_http_methods(['POST'])
def api(request):
    # check sign
    if notify_verify(request.POST):
        method = request.POST.get('method')
        if method == 'getPayment':
            payment = Bill.objects.filter(out_trade_no=request.POST.get('out_trade_no'),)
            if payment:
                return HttpResponse(serializers.serialize("json", payment.as_list()), content_type="application/json")
        elif method == 'getUser':
            user = Buyer.objects.filter(buyer_id=request.POST.get('buyer_id'))
            if user:
                return HttpResponse(serializers.serialize("json", user.as_list()), content_type="application/json")
        elif method == 'getPaymentByUser':
            bills = Bill.objects.filter(buyer_id=request.POST.get('buyer_id'))
            if bills:
                return HttpResponse(serializers.serialize("json", bills.as_list()), content_type="application/json")

    return HttpResponse('false')

@csrf_exempt
def not_url_handler(request):
    logger1.info('notify test')
    if request.POST and request.POST['sign_type']:
        logger1.info(request.POST)
        return HttpResponse('success')    
    else:
        return HttpResponse('fail')
    
@csrf_exempt
@require_http_methods(['GET'])
def list_payment(request):
    bill = Bill.objects.all()
    return render_to_response("list.html", {"bill": bill})
