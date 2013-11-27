from django.db import models
from django.forms.models import model_to_dict

# Create your models here.


class Users(models.Model):
    name = models.TextField(default='Alipay user')
    seller_id = models.IntegerField()
    seller_email = models.EmailField()

    def __unicode__(self):
        return model_to_dict(self)