# -*- coding: utf-8 -*-  

from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponseRedirect  
from django.utils import timezone
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
from utils import wechat

import config
import time
import json
import traceback
import redis
import re
import random
import datetime,time

from django.conf import settings
from utils import http_utils
from users.models import User,verify_code
from coffee.models import coffee,coffee_trade,coffee_coupon
from config import params
from utils.yunpian import YunPian 

def user_register(request):
    #print "@@@@rquest",request.session.keys()
    #del request.session['openid']
    #del request.session['headimgurl']
    #del request.session['access_token']
    #del request.session['country']
    #del request.session['base_expire_in']
    #del request.session['nickname']

    template = 'user_register.html'
    title = '会员注册'
    try:
        if settings.TEST:
            return render_to_response(template,{'title': title}) 
        else:
            if 'access_token' in request.session and 'openid' in request.session:
                access_token = request.session["access_token"]
                openid = request.session["openid"]
                if not access_token is None:
                    user = User.objects.filter(openid=openid)[0]
                    #判断是否为会员，如果已是会员则返回其它页面
                    if user.is_member == 1:
                        template = 'error.html'
                        message = '系统检测您已是会员，快去购买饮品吧'
                        return render_to_response(template,{'message': message,'title':title}) 
                    else:
                        return render_to_response(template,{'title': title}) 
            else:
                url = 'https://open.weixin.qq.com/connect/oauth2/authorize?appid=%s&redirect_uri=%s&response_type=code&scope=snsapi_userinfo&state=1#wechat_redirect'%(config.appid, config.callback)
                return HttpResponseRedirect(url)
    except:
        traceback.print_exc()




#获取短信验证码
@csrf_exempt
def for_sms_code(request):
    mobile = request.POST.get('mobile','')
    mobile = mobile.replace(' ','').replace(' ','')
    if 'access_token' in request.session and 'openid' in request.session:
        access_token = request.session["access_token"]
        if not access_token is None:
            try:
                if mobile:
                    #验证是否为有效手机号
                    mobile_pat = re.compile('^(13\d|14[5|7]|15\d|166|17\d|18\d)\d{8}$')
                    res = re.search(mobile_pat,mobile)
                    if res:
                        #生成手机验证码
                        mobile_code,created = verify_code.objects.get_or_create(mobile=mobile)
                        c = random.randint(1000,9999)
                        mobile_code.code = str(c)
                        mobile_code.save()
                        #如果非第一次创建，则更新生成新验证码的当前时间
                        if created == False:
                            time_now = timezone.now()
                            mobile_code.create_time = time_now
                            mobile_code.save()
                        #发送短信 
                        code = verify_code.objects.filter(mobile = mobile).first().code
                        sms_obj = YunPian(params.APIKEY)
                        msg = sms_obj.send_sms(code = code,mobile = mobile)
                        return HttpResponse(msg)
                    else:
                        return HttpResponse('wrong_format')
                else:
                    return HttpResponse('mobile_blank')
            except:
                traceback.print_exc()
    else:
        url = 'https://open.weixin.qq.com/connect/oauth2/authorize?appid=%s&redirect_uri=%s&response_type=code&scope=snsapi_userinfo&state=1#wechat_redirect'%(config.appid, config.callback)
        return HttpResponseRedirect(url)
        
            
@csrf_exempt
def is_code_right(request):
    try:
        if settings.TEST:
            result = {}
            openid = 'ot3LK1UtJBHJ7RFMgQnzYZS47fd4'
            user = User.objects.get(openid=openid)
            phone_number = user.phone_number
            if phone_number:
                result['status'] = 'duplicated_number'
            #判断该openid users_user是否有手机用户，1 如果有和手机号码参数作比对，相同则提示已有该用户，请勿重复操作，不相同提示您已绑定手机号码，不能再绑定其它号码 2如果没有则执行以下操作
            else:
                mobile = request.POST.get('mobile','')
                code = request.POST.get('code','')
                #去空格
                mobile = mobile.replace(' ','').replace(' ','')
                #验证是否为有效手机号
                mobile_pat = re.compile('^(13\d|14[5|7]|15\d|166|17\d|18\d)\d{8}$')
                res = re.search(mobile_pat,mobile)
                if res:
                    temp = verify_code.objects.get(mobile = mobile)
                    #注册成功，则存储用户信息包括openid,infomation等，分发相应优惠卷
                    time_now = timezone.now()
                    code_create_time = temp.create_time
                    expire_time = code_create_time + datetime.timedelta(minutes=5)
                    #验证码正确
                    if temp.code == str(code):
                        #已过期
                        if time_now > expire_time:
                            result['status'] = 'expire'
                        #未过期
                        else:
                            #将手机号码存入users_user用户表
                            user.phone_number = mobile
                            user.is_member = 1
                            user.save()
                            result['status'] = 'ok'
                            #注册成功后删除此条记录.避免再次利用
                            verify_code.objects.filter(mobile = mobile).delete()
                            #分发优惠卷,目前默认为一张12元卡布奇诺咖啡免费卷，一张8元现泡港式奶茶免费卷，4张5元代金券，2张3元代金券，2张2元代金券，以上代金券均为无门槛卷
                            distributed_coupon(openid)
                    #验证码错误
                    else:
                        result['status'] = 'error'
                else:
                    result['status'] = 'wrong_format' 
            return HttpResponse(json.dumps(result))
        if 'access_token' in request.session and 'openid' in request.session:
            result = {}
            openid = request.session['openid']
            user = User.objects.get(openid=openid)
            phone_number = user.phone_number
            if phone_number:
                result['status'] = 'duplicated_number'
            #判断该openid users_user是否有手机用户，1 如果有和手机号码参数作比对，相同则提示已有该用户，请勿重复操作，不相同提示您已绑定手机号码，不能再绑定其它号码 2如果没有则执行以下操作
            else:
                mobile = request.POST.get('mobile','')
                code = request.POST.get('code','')
                #去空格
                mobile = mobile.replace(' ','').replace(' ','')
                #验证是否为有效手机号
                mobile_pat = re.compile('^(13\d|14[5|7]|15\d|166|17\d|18\d)\d{8}$')
                res = re.search(mobile_pat,mobile)
                if res:
                    temp = verify_code.objects.get(mobile = mobile)
                    #注册成功，则存储用户信息包括openid,infomation等，分发相应优惠卷
                    time_now = timezone.now()
                    code_create_time = temp.create_time
                    expire_time = code_create_time + datetime.timedelta(minutes=5)
                    #验证码正确
                    if temp.code == str(code):
                        #已过期
                        if time_now > expire_time:
                            result['status'] = 'expire'
                        #未过期
                        else:
                            #将手机号码存入users_user用户表
                            user.phone_number = mobile
                            user.is_member = 1
                            user.save()
                            result['status'] = 'ok'
                            #注册成功后删除此条记录.避免再次利用
                            verify_code.objects.filter(mobile = mobile).delete()
                            #分发优惠卷,目前默认为一张12元卡布奇诺咖啡免费卷，一张8元现泡港式奶茶免费卷，4张5元代金券，2张3元代金券，2张2元代金券，以上代金券均为无门槛卷
                            distributed_coupon(openid)
                    #验证码错误
                    else:
                        result['status'] = 'error'
                else:
                    result['status'] = 'wrong_format' 
            return HttpResponse(json.dumps(result))
    except:
        traceback.print_exc()
    
def get_user_info(request):
    pass 



def distributed_coupon(openid):
    try:
        #分发饮品卷
        #temp_list = ['30','37']
        #for temp in temp_list:
        #    trade = coffee_trade(openid=openid,valid=1,trade_date=timezone.now(),count=1,coffee_id=int(temp),flag=1)
        #    trade.save()
        #默认优惠卷有效期30天 
        a = 0
        while a < 2:
            coupon = coffee_coupon(openid=openid,coffee_coupon_number='5.00',user_coupon_validity_date=timezone.now() + datetime.timedelta(days=30))
            coupon.save()
            a += 1

        b = 0
        while b < 4:
            coupon = coffee_coupon(openid=openid,coffee_coupon_number='4.00',user_coupon_validity_date=timezone.now() + datetime.timedelta(days=30))
            coupon.save()
            b += 1

        c = 0
        while c < 4:
            coupon = coffee_coupon(openid=openid,coffee_coupon_number='3.00',user_coupon_validity_date=timezone.now() + datetime.timedelta(days=30))
            coupon.save()
            c += 1
        d = 0
        while d < 6:
            coupon = coffee_coupon(openid=openid,coffee_coupon_number='2.00',user_coupon_validity_date=timezone.now() + datetime.timedelta(days=30))
            coupon.save()
            d += 1
    except:
        traceback.print_exc()


