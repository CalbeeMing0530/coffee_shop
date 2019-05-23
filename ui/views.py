# -*- coding: utf-8 -*-  
import json
import config
import time
import traceback
import datetime,time
import redis
import re

from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponseRedirect
from django.conf import settings  

from utils import wechat
from users.models import User
from coffee.models import coffee
from datetime import date
from utils import http_utils
from config import params

def index(request):
    url = 'https://open.weixin.qq.com/connect/oauth2/authorize?appid=%s&redirect_uri=%s&response_type=code&scope=snsapi_userinfo&state=1#wechat_redirect'%(config.appid, config.callback)
    return HttpResponseRedirect(url)

#回调函数绑定用户
@csrf_exempt
def callback(request):
    try:
        import re
        regex = re.compile('^HTTP_')
        print dict((regex.sub('', header), value) for (header, value) 
               in request.META.items() if header.startswith('HTTP_'))
        if settings.TEST:
            pass
        else:
            if not 'code' in request.GET:
                return HttpResponse("参数不正确")
            code = request.GET['code']
            token = wechat.get_access_token(code)
            access_token = token['access_token']
            expires_in = token['expires_in']
            openid = token['openid']
            userinfo = wechat.get_user_info(access_token, openid) 
            if 'errmsg' in userinfo:
                return HttpResponse(u'返回参数不正确，微信服务器异常:%s'%userinfo['errmsg'])
            province = userinfo['province'].encode('raw_unicode_escape')
            headimgurl = userinfo['headimgurl']
            city = userinfo['city'].encode('raw_unicode_escape')
            country = userinfo['country'].encode('raw_unicode_escape')
            sex = userinfo['sex']
            nickname = userinfo['nickname'].encode('raw_unicode_escape')

            print "@@@@province",province
            print "@@@@headimgurl",headimgurl
            print "@@@@city",city
            print "@@@@country",country
            print "@@@@sex",sex
            print "@@@@nickname",nickname

            
            if len(User.objects.filter(openid=openid)) == 0:
                user = User(openid = openid, nickname = nickname, user_image = headimgurl, province = province, city = city,country = country, sex = sex,is_subscribe=1)
                user.save()
            
            #获取基础accesstoken，存session
            base_token = wechat.get_base_access_token()
            print "@@@@@@@@@@@base_token",base_token
            base_access_token = base_token['access_token']
            base_expire_in = base_token['expires_in']
            time_now = get_time_now()
            base_expire_in = time_now + int(base_expire_in)
            request.session['access_token'] = base_access_token
            request.session['base_expire_in'] = base_expire_in
            request.session['openid'] = openid
            request.session['nickname'] = nickname
            request.session['headimgurl'] = headimgurl
            request.session['country'] = country
           
            template = 'user_register.html' 
            title = '会员注册'
            #drinking_type = 'coffee'
            #coffee_info = coffee.objects.filter(coffee_type=1)
            #return render_to_response(template,{'title': title,'coffee_info':coffee_info,'drinking_type':drinking_type})
            return render_to_response(template,{'title': title})
        
        url = 'https://open.weixin.qq.com/connect/oauth2/authorize?appid=%s&redirect_uri=%s&response_type=code&scope=snsapi_userinfo&state=1#wechat_redirect'%(config.appid, config.callback)
        return HttpResponseRedirect(url)
    except:
        traceback.print_exc()




#获取当前时间戳
def get_time_now():
    time_now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    time_now = time.strptime(time_now,"%Y-%m-%d %H:%M:%S")
    time_now = int(time.mktime(time_now))
    return time_now 
