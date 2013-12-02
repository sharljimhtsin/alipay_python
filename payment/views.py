#-*- coding:utf-8 -*-

from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
import httplib
import urllib
import json

from alipay.alipay import *
from payment.models import Bill, Notify
from accounts.models import Buyer
from settings import LOGGING_PAYMENT


logger1 = logging.getLogger(__name__)
logger1.setLevel(logging.INFO)
logger1.addHandler(logging.FileHandler(LOGGING_PAYMENT))

from django.views.decorators.csrf import csrf_exempt


@csrf_exempt
def notify_url_handler(request):
    """
    Handler for notify_url for asynchronous updating billing information.
    Logging the information.
    """
    logger1.info('>>notify url handler start...')
    if request.method == 'POST':
        logger1.info(request.POST)
        if notify_verify(request.POST):
            logger1.info('pass verification...')
            # save the bill
            bill = Bill(out_trade_no=request.POST.get('out_trade_no'),
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

            # save the user
            users = Users.objects.get(seller_id=request.POST.get('seller_id'))
            if users:
                users = Users(name='',
                              seller_id=bill.seller_id,
                              seller_email=bill.seller_email)
                users.save()

            # save this notify
            notify = Notify(time=request.POST.get('time'),
                            type=request.POST.get('type'),
                            nid=request.POST.get('nid'),
                            sign_type=request.POST.get('sign_type'),
                            sign=request.POST.get('sign'),
                            bill=bill.pk)
            notify.save()

            return HttpResponse('success')
    return HttpResponse("fail")


def return_url_handler(request):
    """
    Handler for synchronous updating billing information.
    """
    logger1.info('>> return url handler start')
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
def notify(domain, url, params):
    con = httplib.HTTPConnection(domain)
    param = urllib.urlencode(params)
    con.request('POST', url, param)
    resp = con.getresponse()


def api(request):
    # check sign
    if notify_verify(request.POST):
        method = request.POST.get('method')
        if method == 'getPayment':
            payment = Bill.objects.get(out_trade_no=request.POST.get('out_trade_no'))
            if payment:
                return HttpResponse(json.dumps(payment), content_type="application/json")
        elif method == 'getUser':
            users = Buyer.objects.get(buyer_id=request.POST.get('buyer_id'))
            if users:
                return HttpResponse(json.dumps(users), content_type="application/json")
        elif method == 'getPaymentByUser':
            users = Buyer.objects.get(buyer_id=request.POST.get('buyer_id'))

    return HttpResponse('false')