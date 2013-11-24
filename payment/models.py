#-*- coding:utf-8 -*-

from django.db import models
from django.contrib import admin
import datetime


class Bill(models.Model):
    account_type = models.CharField(max_length=20, default='free', null=True)
    trade_status = models.CharField(max_length=50, default='INIT', null=True)
    start_date = models.DateTimeField(default=datetime.datetime(1900, 1, 1))
    expire_date = models.DateTimeField(default=datetime.datetime(1900, 1, 1))

    def __unicode__(self):
        return self.user.username + " " + self.account_type


admin.site.register(Bill)
