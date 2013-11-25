from django.db import models

# Create your models here.


class Users(models.Model):
    name = models.CharField(max_length=20)
    seller_id = models.CharField(max_length=30, null=True)
    seller_email = models.CharField(max_length=100, null=True)