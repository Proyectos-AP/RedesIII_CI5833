from django.db import models

# Create your models here.
# class Client(models.Model):
#     username = models.CharField(max_length=200)
#     password = models.CharField(max_length=200)
#     logged_in = models.BooleanField(default=False)
#     login_try = models.IntegerField(default=0)
#     blocked = models.BooleanField(default=False)


class Product(models.Model):
    description = models.CharField(max_length=200)
    amount = models.DecimalField(max_digits=20,decimal_places=2)
    vendor = models.CharField(max_length=10,default="")
