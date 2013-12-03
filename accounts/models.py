from django.db import models
from django.forms.models import model_to_dict

# Create your models here.


class Seller(models.Model):
    name = models.TextField(default='Alipay user')
    seller_id = models.IntegerField()
    seller_email = models.EmailField()

    def __unicode__(self):
        return model_to_dict(self)


class Buyer(models.Model):
    name = models.TextField(default='Alipay user')
    buyer_id = models.TextField()
    buyer_email = models.EmailField()

    def __unicode__(self):
        return model_to_dict(self)


class Partner(models.Model):
    name = models.TextField()
    app_name = models.TextField()
    app_id = models.BigIntegerField()
    public_key = models.TextField()
    notify_url = models.TextField()
    return_url = models.TextField()