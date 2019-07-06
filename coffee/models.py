from __future__ import unicode_literals
from django.db import models
from datetime import datetime
import django.utils.timezone


# Create your models here.
class coffee(models.Model):
    coffee_id = models.AutoField(primary_key=True)
    coffee_en_name  = models.CharField(max_length=255, unique=True,blank=False)
    coffee_name = models.CharField(max_length=255, unique=True,blank=False)
    coffee_price = models.CharField(max_length=255,blank=False)
    coffee_image = models.CharField(max_length=255,blank=False)
    coffee_type = models.CharField(max_length=255,blank=False)
    coffee_code = models.IntegerField()
    coffee_origin_price = models.CharField(max_length=255,blank=False)
    package_code = models.CharField(max_length=255,blank=False)
    coffee_concentration = models.IntegerField()
    order_by_id = models.IntegerField()


class coffee_trade(models.Model):
    #coffee_en_name  = models.CharField(max_length=255)
    #coffee_name = models.CharField(max_length=255)
    coffee_id = models.CharField(max_length=255)
    openid = models.CharField(max_length=40, default=None)
    valid = models.IntegerField(default=0)
    trade_date = models.DateTimeField(default=django.utils.timezone.now)
    count = models.IntegerField()
    flag = models.IntegerField(default=0)
    #fee = models.CharField(max_length=255)

class coffee_order(models.Model):
    order_id = models.AutoField(primary_key=True)
    openid = models.CharField(max_length=40, default=None)
    trade_date = models.DateTimeField(default=django.utils.timezone.now)
    total_fee  = models.CharField(max_length=255)
    valid = models.IntegerField(default=0)
    coffee_info = models.CharField(max_length=65533)

class coffee_coupon(models.Model):
    openid = models.CharField(max_length=40, default=None)
    coffee_coupon_number = models.CharField(max_length=1024, default=None)
    user_coupon_validity_date = models.DateTimeField()
    
class coffee_code(models.Model):
    openid = models.CharField(max_length=40, default=None)
    coffee_en_name  = models.CharField(max_length=255)
    coffee_name = models.CharField(max_length=255)
    coffee_code = models.CharField(max_length=255)
    #flag = models.IntegerField(default=0)
    type = models.IntegerField(default=1)
    coffee_code_id = models.IntegerField()
    coffee_id = models.IntegerField()
    coffee_code_order_id = models.CharField(max_length=255)

class Coupon(models.Model):
    coupon_id = models.AutoField(primary_key=True)
    coupon_price = models.CharField(max_length=255,blank=False)
