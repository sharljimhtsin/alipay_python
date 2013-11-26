from django.db import models

# Create your models here.


class Users(models.Model):
    name = models.TextField()
    seller_id = models.IntegerField()
    seller_email = models.EmailField()