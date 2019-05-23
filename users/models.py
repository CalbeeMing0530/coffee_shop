from __future__ import unicode_literals
from datetime import datetime
from django.db import models
import django.utils.timezone
# Create your models here.


#class User(models.Model):
#    openid = models.CharField(max_length=40, default=None)
#    user_image = models.CharField(max_length=255, null=True, blank=False)
#    province = models.CharField(max_length=255, null=True, blank=False)
#    city = models.CharField(max_length=255, null=True, blank=False)
#    country = models.CharField(max_length=255, null=True, blank=False)
#    sex = models.CharField(max_length=255, null=True, blank=False)
#    nickname = models.CharField(max_length=255, null=True, blank=False)
#    #is_subscribe = models.IntegerField(max_length=10,null=True,blank=False,default=0)

class User(models.Model):
    openid = models.CharField(max_length=40, default=None)
    user_image = models.CharField(max_length=255, null=True, blank=False)
    province = models.CharField(max_length=255, null=True, blank=False)
    city = models.CharField(max_length=255, null=True, blank=False)
    country = models.CharField(max_length=255, null=True, blank=False)
    sex = models.CharField(max_length=255, null=True, blank=False)
    nickname = models.CharField(max_length=255, null=True, blank=False)
    phone_number = models.CharField(max_length=255, null=True, blank=False)
    is_subscribe = models.IntegerField(null=True,blank=False,default=0)
    subscribe_date = models.DateTimeField(default=django.utils.timezone.now)
    is_member = models.IntegerField(default=0)
    role = models.CharField(max_length=255, null=True, blank=False)


class verify_code(models.Model):
    mobile = models.CharField(max_length=255, default=None)
    code = models.CharField(max_length=255, default=None)
    create_time = models.DateTimeField(default=django.utils.timezone.now)
    



#class User_device(models.Model):
#    openid = models.CharField(max_length=40, default=None)
#    hashcode = models.CharField(max_length=255, null=True, blank=False)
#    hashName = models.CharField(max_length=1024, null=True, blank=False)
