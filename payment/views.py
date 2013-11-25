#-*- coding:utf-8 -*-

from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
import logging

from alipay.alipay import *
from payment.models import Bill
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
        if notify_verify(request.POST):
            logger1.info('pass verification...')
            bill = Bill(out_trade_no=request.POST.get('out_trade_no'))
            #TODO:fill obj
            bill.save()
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
    bill = Bill.objects.get(out_trade_no=request.POST.get('out_trade_no'))
    if not bill:
        return HttpResponse('ok')
    else:
        return HttpResponse('null')


def index(request):
    return HttpResponse('home')