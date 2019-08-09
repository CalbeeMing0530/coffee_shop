#!/usr/bin/python
# -*- coding: utf-8 -*-

from utils.yunpian2 import YunPian
from config import params

import os,django
os.environ['DJANGO_SETTING_MODULE']='wechat_site.settings'
django.setup()

from users.models import User

if __name__ == '__main__':
    sms_obj = YunPian(params._SALE_APIKEY)
    phone_number = User.objects.filter(is_member=1).values("phone_number")
    count = User.objects.filter(is_member=1).values("phone_number").count()
    mobile = ""
    str_phone = ""
    test_phone = "15829705510"
    #优惠券面额
    coupon_price = '2.00'
    #优惠券张数
    coupon_count = '2'
    if phone_number:
        for phone in phone_number:
            str_phone += str(phone.get('phone_number','')) + ','
    	#mobile = str_phone[:-1]
	mobile = test_phone
        msg = sms_obj.send_coupon_sms(coupon_price,coupon_count,mobile)	
	print "msg",msg
    else:
       pass 

