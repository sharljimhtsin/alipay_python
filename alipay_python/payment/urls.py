#!/usr/bin/python
from django.conf.urls import patterns, url


urlpatterns = patterns('',
                       url(r'^api$', view='alipay_python.payment.views.api', name="payment_api"),
                       url(r'^return_url$', view='alipay_python.payment.views.return_url_handler', name="payment_return_url"),
                       url(r'^notify_url$', view='alipay_python.payment.views.notify_url_handler', name="payment_notify_url"),
                       url(r'^not$', view='alipay_python.payment.views.not_url_handler', name="test_notify_url"),
                       url(r'^list$', view='alipay_python.payment.views.list_payment', name="list_payment"),
                       url(r'^.*$', view='alipay_python.payment.views.index', name="payment_index"),
)
