#!/usr/bin/python

from django.conf.urls.defaults import *
from django.views.generic.simple import direct_to_template

urlpatterns = patterns('',
                       url(r'^.?$', view='payment.views.index', name="payment_index"),
                       url(r'^api$', view='payment.views.api', name="payment_api"),
                       url(r'^success/$', direct_to_template, {'template': 'payment/success.html'},
                           name="payment_success"),
                       url(r'^error/$', direct_to_template, {'template': 'payment/error.html'}, name="payment_error"),
                       url(r'^return_url$', view='payment.views.return_url_handler', name="payment_return_url"),
                       url(r'^notify_url$', view='payment.views.notify_url_handler', name="payment_notify_url"),
)
