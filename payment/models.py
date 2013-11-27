#-*- coding:utf-8 -*-

from django.db import models
from django.contrib import admin
from django.forms.models import model_to_dict


class Bill(models.Model):
    out_trade_no = models.CharField(max_length=64, null=True)
    subject = models.CharField(max_length=256, null=True)
    type = models.CharField(max_length=4, null=True)
    trade_no = models.CharField(max_length=64, null=True)
    trade_status = models.CharField(max_length=10, null=True)
    seller_id = models.CharField(max_length=30, null=True)
    seller_email = models.CharField(max_length=100, null=True)
    buyer_id = models.CharField(max_length=30, null=True)
    buyer_email = models.CharField(max_length=100, null=True)
    total_fee = models.BigIntegerField(null=True)
    quantity = models.SmallIntegerField(null=True)
    price = models.BigIntegerField(null=True)
    body = models.CharField(max_length=400, null=True)
    gmt_create = models.DateTimeField(null=True)
    gmt_payment = models.DateTimeField(null=True)
    is_total_fee_adjust = models.CharField(max_length=1, null=True)
    use_coupon = models.CharField(max_length=1, null=True)
    discount = models.CharField(max_length=10, null=True)

    def __unicode__(self):
        return model_to_dict(self)


class Notify(models.Model):
    time = models.DateTimeField()
    type = models.CharField(max_length=20)
    nid = models.CharField(max_length=50)
    sign_type = models.CharField(max_length=3, default='RSA')
    sign = models.CharField(max_length=100)
    bill = models.ForeignKey(Bill)

    def __unicode__(self):
        return model_to_dict(self)


admin.site.register(Bill)
admin.site.register(Notify)
