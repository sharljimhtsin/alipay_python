#!/usr/bin/python

from django.conf.urls.defaults import *

urlpatterns = patterns('',
                       url(r'^api$', view='payment.views.api', name="payment_api"),
                       url(r'^return_url$', view='payment.views.return_url_handler', name="payment_return_url"),
                       url(r'^notify_url$', view='payment.views.notify_url_handler', name="payment_notify_url"),
                       url(r'^.*$', view='payment.views.index', name="payment_index"),
)
