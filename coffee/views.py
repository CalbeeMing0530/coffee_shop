# -*- coding: utf-8 -*-  

from django.shortcuts import render
from django.http import HttpResponse,HttpResponseServerError,HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.utils import timezone

from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
from utils import wechat
from django.conf import settings
from utils import http_utils
from users.models import User
from coffee.models import coffee,coffee_trade,coffee_code,coffee_order,coffee_coupon,Coupon
from wechat_sdk.wechatAPI import WechatOrder,WechatAPI,WechatPayAPI
from config import params

import config
import time
import json
import traceback
import random,string
import redis
import traceback
import datetime,time



# Create your views here.
#咖啡单品
def coffee_item(request):
    template = 'coffee_item.html' 
    title = '咖啡单品'
    drinking_type = 'coffee'
    try:
        if settings.TEST:
            #print request.session.keys()
            #p = coffee(coffee_en_name="Iced Lemon Coffee",coffee_name="冰柠咖啡",coffee_price='12.00',activity_price='12.00',coffee_image='cold_Lemon_coffee.png',coffee_code='776',coffee_type=1)
            #p.save()
            #coffee.objects.filter(coffee_id=57).update(coffee_en_name='经典美式咖啡 * 1 + 澳白 * 1 + 抹茶拿铁咖啡 * 1 + 摩卡 * 1 + 卡布奇诺 * 1 + 拿铁 * 1')
            #coffee.objects.filter(coffee_id=59).update(coffee_en_name='澳白 * 1 + 抹茶拿铁咖啡 * 1')
            #coffee.objects.filter(coffee_id=60).update(coffee_en_name='经典美式咖啡 * 1 + 摩卡 * 1 + 拿铁 * 1')
            #coffee.objects.filter(coffee_id=61).update(coffee_en_name='摩卡 * 1 + 卡布奇诺 * 1 + 玛琪雅朵 * 1 + 拿铁 * 1')
            #coffee.objects.filter(coffee_id=62).update(coffee_en_name='经典美式咖啡 * 7')
            #coffee.objects.filter(coffee_id=63).update(coffee_en_name='经典美式咖啡(无糖) * 7')
            #coffee.objects.filter(coffee_id=64).update(coffee_en_name='拿铁 * 7')
            #coffee.objects.filter(coffee_id=65).update(coffee_en_name='经典美式咖啡 * 22')
            #coffee.objects.filter(coffee_id=66).update(coffee_en_name='经典美式咖啡(无糖) * 22')
            #coffee.objects.filter(coffee_id=67).update(coffee_en_name='冰柠咖啡 * 1 + 柠檬冰茶 * 1')
            #coffee.objects.filter(coffee_id=68).update(coffee_en_name='冰美式 * 1 + 冰卡布奇诺 * 1+冰拿铁 * 1')
            #coffee.objects.filter(coffee_id=68).update(coffee_en_name='冰美式 * 1 + 冰卡布奇诺 * 1+冰拿铁 * 1')
            coffee_info = coffee.objects.filter(coffee_type=1).order_by('-order_by_id')
            return render_to_response(template,{'title':title,'coffee_info':coffee_info,'drinking_type':drinking_type}) 
        else:
            if 'access_token' in request.session and 'openid' in request.session:
                access_token = request.session["access_token"]
                if not access_token is None:
                    coffee_info = coffee.objects.filter(coffee_type=1).order_by('-order_by_id')
                    #p = coffee(coffee_en_name="Iced Americano(no sugar)",coffee_name="冰美式(无糖)",coffee_price='8.00',coffee_origin_price='8.00',coffee_image='hot_matcha.png',coffee_code='931',coffee_type=1)
                    #p.save()
                    return render_to_response(template,{'title':title,'coffee_info':coffee_info,'drinking_type':drinking_type}) 
            else:
                url = 'https://open.weixin.qq.com/connect/oauth2/authorize?appid=%s&redirect_uri=%s&response_type=code&scope=snsapi_userinfo&state=1#wechat_redirect'%(config.appid, config.callback)
                return HttpResponseRedirect(url)
    except:
        traceback.print_exc()
        template = 'error.html'
        title = '获取数据失败'
        return render_to_response(template,{'title': title}) 




#茶饮单品
def tea_item(request):
    template = 'coffee_item.html' 
    title = '茶饮单品'
    drinking_type = 'tea'
    try:
        if settings.TEST:
            coffee_info = coffee.objects.filter(coffee_type=2).order_by('-order_by_id')
            return render_to_response(template,{'title': title,'coffee_info':coffee_info,'drinking_type':drinking_type}) 
        else:
            if 'access_token' in request.session and 'openid' in request.session:
                access_token = request.session["access_token"]
                if not access_token is None:
                    coffee_info = coffee.objects.filter(coffee_type=2).order_by('-order_by_id')
                    return render_to_response(template,{'title':title,'coffee_info':coffee_info,'drinking_type':drinking_type}) 
            else:
                url = 'https://open.weixin.qq.com/connect/oauth2/authorize?appid=%s&redirect_uri=%s&response_type=code&scope=snsapi_userinfo&state=1#wechat_redirect'%(config.appid, config.callback)
                return HttpResponseRedirect(url)
    except:
        traceback.print_exc()
        template = 'error.html'
        title = '获取数据失败'
        return render_to_response(template,{'title': title}) 


       
#套餐
def package(request):
    template = 'coffee_item.html' 
    title = '套餐优惠'
    drinking_type = 'package'
    try:
        if settings.TEST:
            coffee_info = coffee.objects.filter(coffee_type=3).order_by('-order_by_id')
            return render_to_response(template,{'title': title,'coffee_info':coffee_info,'drinking_type':drinking_type}) 
        else:
            if 'access_token' in request.session and 'openid' in request.session:
                access_token = request.session["access_token"]
                if not access_token is None:
                    coffee_info = coffee.objects.filter(coffee_type=3).order_by('-order_by_id')
                    return render_to_response(template,{'title':title,'coffee_info':coffee_info,'drinking_type':drinking_type}) 
            else:
                url = 'https://open.weixin.qq.com/connect/oauth2/authorize?appid=%s&redirect_uri=%s&response_type=code&scope=snsapi_userinfo&state=1#wechat_redirect'%(config.appid, config.callback)
                return HttpResponseRedirect(url)
    except:
        traceback.print_exc()
        template = 'error.html'
        title = '获取数据失败'
        return render_to_response(template,{'title': title}) 


#寻找附近的咖啡吧
def search_coffeebar_nearby(request):
    template = 'search_coffeebar_nearby.html'
    title = '附近的咖啡吧'
    try:
        if settings.TEST:
            return render_to_response(template,{'title': title}) 
        else:
            if 'access_token' in request.session and 'openid' in request.session:
                access_token = request.session["access_token"]
                if not access_token is None:
                    return render_to_response(template,{'title': title}) 
            else:
                url = 'https://open.weixin.qq.com/connect/oauth2/authorize?appid=%s&redirect_uri=%s&response_type=code&scope=snsapi_userinfo&state=1#wechat_redirect'%(config.appid, config.callback)
                return HttpResponseRedirect(url)
    except:
        traceback.print_exc()

#个人中心 我的主页
def user_center(request):
    template = 'user_center.html' 
    title = '我的主页'
    try:
        if settings.TEST:
            user = User.objects.filter(openid='o7go2597XriiWy4cgMWG_y3y7Bag')[0]
            return render_to_response(template,{'title': title,'user':user}) 
        else:
            if 'access_token' in request.session and 'openid' in request.session:
                access_token = request.session["access_token"]
                openid = request.session["openid"]
                user = User.objects.filter(openid=openid)[0]
                if not access_token is None:
                    return render_to_response(template,{'title': title,'user':user}) 
            else:
                url = 'https://open.weixin.qq.com/connect/oauth2/authorize?appid=%s&redirect_uri=%s&response_type=code&scope=snsapi_userinfo&state=1#wechat_redirect'%(config.appid, config.callback)
                return HttpResponseRedirect(url)
    except:
        traceback.print_exc()
        template = 'error.html'
        title = '获取数据失败'
        return render_to_response(template,{'title': title}) 


#个人中心 饮品设置
def drinking_setting(request):
    template = 'drinking_setting.html' 
    title = '饮品设置'
    try:
        if settings.TEST:
            coffee_temp = coffee.objects.all()
            user = User.objects.filter(openid='o7go2597XriiWy4cgMWG_y3y7Bag')[0]
            return render_to_response(template,{'title': title,'coffee_info':coffee_temp,'user':user}) 
        else:
            if 'access_token' in request.session and 'openid' in request.session:
                access_token = request.session["access_token"]
                openid = request.session["openid"]
                user = User.objects.filter(openid=openid)[0]
                coffee_temp = coffee.objects.all()
                if not access_token is None:
                    return render_to_response(template,{'title': title,'coffee_info':coffee_temp,'user':user}) 
            else:
                url = 'https://open.weixin.qq.com/connect/oauth2/authorize?appid=%s&redirect_uri=%s&response_type=code&scope=snsapi_userinfo&state=1#wechat_redirect'%(config.appid, config.callback)
                return HttpResponseRedirect(url)
    except:
        traceback.print_exc()
        template = 'error.html'
        title = '获取数据失败'
        return render_to_response(template,{'title': title}) 


#编辑饮品页面
def edit_drinking(request,drinking_id):
    template = 'edit_drinking.html'
    title = '编辑饮品'
    try:
        if settings.TEST: 
            coffee_info = coffee.objects.filter(coffee_id=drinking_id)[0]
            return render_to_response(template,{'title': title,'coffee_info':coffee_info})
        else:
            if 'access_token' in request.session and 'openid' in request.session:
                coffee_info = coffee.objects.filter(coffee_id=drinking_id)[0]
                return render_to_response(template,{'title': title,'coffee_info':coffee_info})
            else:
                url = 'https://open.weixin.qq.com/connect/oauth2/authorize?appid=%s&redirect_uri=%s&response_type=code&scope=snsapi_userinfo&state=1#wechat_redirect'%(config.appid, config.callback)
                return HttpResponseRedirect(url)
    except:
        traceback.print_exc()
        template = 'error.html'
        title = '获取数据失败'
        return render_to_response(template,{'title': title}) 


#编辑饮品信息
@csrf_exempt
def edit_drinking_info(request):
    try:
        data = request.POST 
        dringking_id = data.get('dringking_id')
        coffee_name = data.get('coffee_name')
        coffee_en_name = data.get('coffee_en_name')
        coffee_price = data.get('coffee_price')
        coffee_origin_price = data.get('coffee_origin_price')
        coffee_concentration = data.get('coffee_concentration')
        order_by_id = data.get('order_by_id')
        coffee_exist = coffee.objects.filter(coffee_id=dringking_id).count()
        res = {}
        #是否存在此咖啡种类
        if coffee_exist > 0:
            coffee.objects.filter(coffee_id=dringking_id).update(coffee_name=coffee_name)
            coffee.objects.filter(coffee_id=dringking_id).update(coffee_en_name=coffee_en_name)
            coffee.objects.filter(coffee_id=dringking_id).update(coffee_origin_price=coffee_origin_price)
            coffee.objects.filter(coffee_id=dringking_id).update(coffee_price=coffee_price)
            coffee.objects.filter(coffee_id=dringking_id).update(order_by_id=int(order_by_id))
            coffee.objects.filter(coffee_id=dringking_id).update(coffee_concentration=int(coffee_concentration))
            res["status"] = "ok"
        else:
            res["status"] = "error"
        return HttpResponse(json.dumps(res))
    except:
        traceback.traceback

#个人中心 - 我的咖啡
def my_coffee_coupon(request):
    template = 'my_coffee_coupon.html' 
    title = '我的咖啡'
    try:
        if settings.TEST:
            coffee_infos = coffee_trade.objects.raw('select count(*) as coffee_count,coffee_id,id from coffee_coffee_trade where openid="o7go2597XriiWy4cgMWG_y3y7Bag" and flag=0 group by coffee_id')
            res = [] 
            openid = 'o7go2597XriiWy4cgMWG_y3y7Bag'
            for coffee_info in coffee_infos:
                coffee_temp = coffee.objects.get(coffee_id=coffee_info.coffee_id)
                coffee_dict = {}
                coffee_dict['coffee_count'] = coffee_info.coffee_count
                coffee_dict['coffee_name'] = coffee_temp.coffee_name
                coffee_dict['coffee_en_name'] = coffee_temp.coffee_en_name
                coffee_dict['coffee_image'] = coffee_temp.coffee_image
                coffee_dict['coffee_id'] = coffee_info.coffee_id
                #判断是否已领取
                coffee_code_temp = coffee_code.objects.filter(coffee_en_name=coffee_temp.coffee_en_name,openid=openid,type=1).count()
                if int(coffee_code_temp) == coffee_info.coffee_count:
                    btn_value = "查看提货码"
                else:
                    btn_value = "获取提货码"
                coffee_dict['btn_value'] = btn_value
                res.append(coffee_dict)
            user = User.objects.filter(openid=openid)[0]
            return render_to_response(template,{'title': title,'res':json.dumps(res),'user':user}) 
        else:
            if 'access_token' in request.session and 'openid' in request.session:
                access_token = request.session["access_token"]
                openid = request.session["openid"]
                if not access_token is None:
                    coffee_infos = coffee_trade.objects.raw('select count(*) as coffee_count,coffee_id,id from coffee_coffee_trade where openid="'+openid+'" and flag=0 group by coffee_id')
                    res = [] 
                    for coffee_info in coffee_infos:
                        print "@@@@@coffee_info.coffee_id",coffee_info.coffee_id
                        coffee_temp = coffee.objects.get(coffee_id=coffee_info.coffee_id)
                        coffee_dict = {}
                        code_dict = {}
                        coffee_dict['coffee_count'] = coffee_info.coffee_count
                        coffee_dict['coffee_name'] = coffee_temp.coffee_name
                        coffee_dict['coffee_en_name'] = coffee_temp.coffee_en_name
                        coffee_dict['coffee_image'] = coffee_temp.coffee_image
                        coffee_dict['coffee_id'] = coffee_info.coffee_id
                        #判断是否已领取
                        coffee_code_temp = coffee_code.objects.filter(coffee_en_name=coffee_temp.coffee_en_name,openid=openid,type=1).count()
                        if int(coffee_code_temp) == coffee_info.coffee_count:
                            btn_value = "查看提货码"
                        else:
                            btn_value = "获取提货码"
                        coffee_dict['btn_value'] = btn_value
                        res.append(coffee_dict)
                    user = User.objects.filter(openid=openid)[0]
                    return render_to_response(template,{'title': title,'res':json.dumps(res),'user':user}) 
            else:
                url = 'https://open.weixin.qq.com/connect/oauth2/authorize?appid=%s&redirect_uri=%s&response_type=code&scope=snsapi_userinfo&state=1#wechat_redirect'%(config.appid, config.callback)
                return HttpResponseRedirect(url)
    except:
        traceback.print_exc()
        template = 'error.html'
        title = '获取数据失败'
        return render_to_response(template,{'title': title}) 


           

#个人中心 - 我的优惠卷
def coupon(request):
    template = 'coupon.html'
    title = '我的优惠券'
    try:
        if settings.TEST:
            #获取代金券
            openid = 'o7go2597XriiWy4cgMWG_y3y7Bag'
            #获取商家赠送代金券
            coupon_infos = coffee_coupon.objects.raw('select count(*) as coupon_count,coffee_coupon_number,id from coffee_coffee_coupon where openid ="o7go2597XriiWy4cgMWG_y3y7Bag" group by coffee_coupon_number')
            res_coupon = []
            for coupon_info in coupon_infos:
                coupon_dict = {}
                coupon_dict['coffee_coupon_number'] = coupon_info.coffee_coupon_number
                coupon_dict['coupon_count'] = coupon_info.coupon_count
                #coupon_dict['user_coupon_validity_date'] = coupon_info.user_coupon_validity_date
                res_coupon.append(coupon_dict)
 
            #获取饮品卷 coffee_trade表中flag=1代表为商家赠送的饮品卷
            coffee_infos = coffee_trade.objects.raw('select count(*) as coffee_count,coffee_id,id from coffee_coffee_trade where openid="o7go2597XriiWy4cgMWG_y3y7Bag" and flag=1 group by coffee_id')
            res = [] 
            for coffee_info in coffee_infos:
                coffee_temp = coffee.objects.get(coffee_id=coffee_info.coffee_id)
                coffee_dict = {}
                coffee_dict['coffee_count'] = coffee_info.coffee_count
                coffee_dict['coffee_name'] = coffee_temp.coffee_name
                coffee_dict['coffee_en_name'] = coffee_temp.coffee_en_name
                coffee_dict['coffee_image'] = coffee_temp.coffee_image
                coffee_dict['coffee_id'] = coffee_info.coffee_id
                #判断是否已领取
                coffee_code_temp = coffee_code.objects.filter(coffee_en_name=coffee_temp.coffee_en_name,openid=openid,type=2).count()
                if int(coffee_code_temp) == coffee_info.coffee_count:
                    btn_value = "查看提货码"
                else:
                    btn_value = "获取提货码"
                coffee_dict['btn_value'] = btn_value
                res.append(coffee_dict)
	    
            user = User.objects.filter(openid=openid)[0]
            return render_to_response(template,{'title': title,'res':json.dumps(res),'user':user,'res_coupon':json.dumps(res_coupon)}) 
        else:
            if 'access_token' in request.session and 'openid' in request.session:
                access_token = request.session["access_token"]
                print "@@@@@@@@@@@@@@@@",access_token
                if not access_token is None:
                    #获取代金券
                    openid = request.session["openid"]
                    #获取商家赠送代金券
                    coupon_infos = coffee_coupon.objects.raw('select count(*) as coupon_count,coffee_coupon_number,id from coffee_coffee_coupon where openid ="'+openid+'" group by coffee_coupon_number')
                    res_coupon = []
                    for coupon_info in coupon_infos:
                        coupon_dict = {}
                        coupon_dict['coffee_coupon_number'] = coupon_info.coffee_coupon_number
                        coupon_dict['coupon_count'] = coupon_info.coupon_count
                        #coupon_dict['user_coupon_validity_date'] = coupon_info.user_coupon_validity_date
                        res_coupon.append(coupon_dict)
 
                    #获取饮品卷 coffee_trade表中flag=1代表为商家赠送的饮品卷
                    coffee_infos = coffee_trade.objects.raw('select count(*) as coffee_count,coffee_id,id from coffee_coffee_trade where openid="'+openid+'" and flag=1 group by coffee_id')
                    res = [] 
                    for coffee_info in coffee_infos:
                        coffee_temp = coffee.objects.get(coffee_id=coffee_info.coffee_id)
                        coffee_dict = {}
                        coffee_dict['coffee_count'] = coffee_info.coffee_count
                        coffee_dict['coffee_name'] = coffee_temp.coffee_name
                        coffee_dict['coffee_en_name'] = coffee_temp.coffee_en_name
                        coffee_dict['coffee_image'] = coffee_temp.coffee_image
                        coffee_dict['coffee_id'] = coffee_info.coffee_id
                        #判断是否已领取
                        coffee_code_temp = coffee_code.objects.filter(coffee_en_name=coffee_temp.coffee_en_name,openid=openid,type=2).count()
                        if int(coffee_code_temp) == coffee_info.coffee_count:
                            btn_value = "查看提货码"
                        else:
                            btn_value = "获取提货码"
                        coffee_dict['btn_value'] = btn_value
                        res.append(coffee_dict)
                    user = User.objects.filter(openid=openid)[0]
                    return render_to_response(template,{'title': title,'res':json.dumps(res),'user':user,'res_coupon':json.dumps(res_coupon)}) 
                    return render_to_response(template,{'title': title}) 
            else:
                url = 'https://open.weixin.qq.com/connect/oauth2/authorize?appid=%s&redirect_uri=%s&response_type=code&scope=snsapi_userinfo&state=1#wechat_redirect'%(config.appid, config.callback)
                return HttpResponseRedirect(url)
    except:
        traceback.print_exc()
        template = 'error.html'
        title = '获取数据失败'
        return render_to_response(template,{'title': title}) 



#个人中心 - 历史订单
def historical_order(request):
    title = '历史订单'
    template = 'historical_order.html'
    try:
        if settings.TEST:
            openid = 'o7go2597XriiWy4cgMWG_y3y7Bag'
            coffee_order_temp = coffee_order.objects.filter(openid=openid,valid=1).order_by('-trade_date')
            user = User.objects.filter(openid=openid)[0]
            return render_to_response(template,{'title': title,'coffee_order_temp':coffee_order_temp,'user':user}) 
        else:
            if 'access_token' in request.session and 'openid' in request.session:
                access_token = request.session["access_token"]
                if not access_token is None:
                    openid = request.session["openid"]  
                    coffee_order_temp = coffee_order.objects.filter(openid=openid,valid=1).order_by('-trade_date')
                    user = User.objects.filter(openid=openid)[0]
                    return render_to_response(template,{'title': title,'coffee_order_temp':coffee_order_temp,'user':user}) 
            else:
                url = 'https://open.weixin.qq.com/connect/oauth2/authorize?appid=%s&redirect_uri=%s&response_type=code&scope=snsapi_userinfo&state=1#wechat_redirect'%(config.appid, config.callback)
                return HttpResponseRedirect(url)
    except:
        traceback.print_exc()
        template = 'error.html'
        title = '获取数据失败'
        return render_to_response(template,{'title': title}) 

#个人中心 - 历史订单
def order_detail(request,order_id=None):
    title = '订单明细'
    template = 'order_detail.html'
    try:
        if settings.TEST:
	    openid = 'o7go2597XriiWy4cgMWG_y3y7Bag'
	    if order_id != 'no_id':
                coffee_order_temp = coffee_order.objects.filter(order_id=order_id,valid=1)
		count = 1
	    else:
		coffee_order_temp = coffee_order.objects.filter(valid=1).order_by('-trade_date')
            	count =  coffee_order.objects.filter(valid=1).order_by('-trade_date').count()
            user = User.objects.filter(openid=openid)[0]
            return render_to_response(template,{'title': title,'coffee_order_temp':coffee_order_temp,'user':user,'count':count}) 
        else:
            if 'access_token' in request.session and 'openid' in request.session:
                access_token = request.session["access_token"]
                if not access_token is None:
                    openid = request.session["openid"]  
		    if order_id != 'no_id':
               	        coffee_order_temp = coffee_order.objects.filter(order_id=order_id,valid=1)
		        count = 1
	    	    else:
			coffee_order_temp = coffee_order.objects.filter(valid=1).order_by('-trade_date')
            	        count =  coffee_order.objects.filter(valid=1).order_by('-trade_date').count()
                    user = User.objects.filter(openid=openid)[0]
                    return render_to_response(template,{'title': title,'coffee_order_temp':coffee_order_temp,'user':user,'count':count}) 
            else:
                url = 'https://open.weixin.qq.com/connect/oauth2/authorize?appid=%s&redirect_uri=%s&response_type=code&scope=snsapi_userinfo&state=1#wechat_redirect'%(config.appid, config.callback)
                return HttpResponseRedirect(url)
    except:
        traceback.print_exc()
        template = 'error.html'
        title = '获取数据失败'
        return render_to_response(template,{'title': title}) 


#个人中心 - 优惠券发放
def dispatch_coupon(request):
    title = '优惠券发放'
    template = 'dispatch_coupon.html'
    try:
        if settings.TEST:
	    openid = 'o7go2597XriiWy4cgMWG_y3y7Bag'
	    template = 'dispatch_coupon.html'
	    #user
	    user = User.objects.filter(openid=openid)[0]
	    res = {}
	    coupons = Coupon.objects.all()
	    #user use coupon 
	    users = User.objects.all()
	    user_coupon = []
	    for v_user in users:
	        _coffee_coupons = coffee_coupon.objects.raw('select id,openid,coffee_coupon_number,count(*) as coupon_count,user_coupon_validity_date from coffee_coffee_coupon where openid="'+v_user.openid+'" group by coffee_coupon_number')	
		user_use_coupon = {}
		for _coffee_coupon in _coffee_coupons:
		    _user = User.objects.filter(openid=_coffee_coupon.openid)[0]
	     	    nick_name = _user.nickname
		    phone_number = _user.phone_number
		    coupon_price = _coffee_coupon.coffee_coupon_number
		    user_use_coupon[""+coupon_price+""] = _coffee_coupon.coupon_count
		    user_use_coupon["nickname"] = nick_name
		    user_use_coupon["phone_number"] = phone_number
		user_coupon.append(user_use_coupon)
	    res["data"] = user_coupon
	    return render_to_response(template,{'title': title,'user':user,'coupons':coupons,'results':json.dumps(res)}) 
        else:
            if 'access_token' in request.session and 'openid' in request.session:
                access_token = request.session["access_token"]
                if not access_token is None:
                    openid = request.session["openid"]  
 	            template = 'dispatch_coupon.html'
	            #user
	            user = User.objects.filter(openid=openid)[0]
	            res = {}
		    coupons = Coupon.objects.all()
	            #user use coupon 
	            users = User.objects.all()
	            user_coupon = []
	            for v_user in users:
	                _coffee_coupons = coffee_coupon.objects.raw('select id,openid,coffee_coupon_number,count(*) as coupon_count,user_coupon_validity_date from coffee_coffee_coupon where openid="'+v_user.openid+'" group by coffee_coupon_number')	
                    	user_use_coupon = {}
	            	for _coffee_coupon in _coffee_coupons:
	            	    _user = User.objects.filter(openid=_coffee_coupon.openid)[0]
	            	    nick_name = _user.nickname
	            	    phone_number = _user.phone_number
	            	    coupon_price = _coffee_coupon.coffee_coupon_number
	            	    user_use_coupon[""+coupon_price+""] = _coffee_coupon.coupon_count
	            	    user_use_coupon["nickname"] = nick_name
	            	    user_use_coupon["phone_number"] = phone_number
	            	user_coupon.append(user_use_coupon)
	            res["data"] = user_coupon
                    return render_to_response(template,{'title': title,'user':user,'coupons':coupons,'results':json.dumps(res)})
            else:
                url = 'https://open.weixin.qq.com/connect/oauth2/authorize?appid=%s&redirect_uri=%s&response_type=code&scope=snsapi_userinfo&state=1#wechat_redirect'%(config.appid, config.callback)
                return HttpResponseRedirect(url)
    except:
        traceback.print_exc()
        template = 'error.html'
        title = '获取数据失败'
        return render_to_response(template,{'title': title}) 

#个人中心 - 添加优惠券页面
def add_coupon(request):
    try:
        if settings.TEST: 
    	    title = '添加优惠券' 
    	    template = "add_coupon.html"
            return render_to_response(template,{'title': title})
        else:
            if 'access_token' in request.session and 'openid' in request.session:
     	    	title = '添加优惠券' 
    	    	template = "add_coupon.html"
            	return render_to_response(template,{'title': title})
            else:
                url = 'https://open.weixin.qq.com/connect/oauth2/authorize?appid=%s&redirect_uri=%s&response_type=code&scope=snsapi_userinfo&state=1#wechat_redirect'%(config.appid, config.callback)
                return HttpResponseRedirect(url)
    except:
        traceback.print_exc()
        template = 'error.html'
        title = '获取数据失败'
        return render_to_response(template,{'title': title}) 

#分发优惠券编辑界面
def dispatch_coupon_operation(request,coupon_price):
    template = 'dispatch_coupon_operation.html'
    title = '优惠券发放数量'
    try:
        if settings.TEST: 
            return render_to_response(template,{'title': title,'coupon_price':coupon_price})
        else:
            if 'access_token' in request.session and 'openid' in request.session:
                return render_to_response(template,{'title': title,'coupon_price':coupon_price})
            else:
                url = 'https://open.weixin.qq.com/connect/oauth2/authorize?appid=%s&redirect_uri=%s&response_type=code&scope=snsapi_userinfo&state=1#wechat_redirect'%(config.appid, config.callback)
                return HttpResponseRedirect(url)
    except:
        traceback.print_exc()
        template = 'error.html'
        title = '获取数据失败'
        return render_to_response(template,{'title': title}) 

#个人中心 - 分发优惠券到所有用户
@csrf_exempt
def dispatch_coupon_to_users(request):
    res = {}
    try:
    	data = request.POST
    	_coupon_price = data.get('coupon_price')
    	_coupon_count = data.get('coupon_count')
	#分发优惠券到所有用户
	users = User.objects.filter(is_member=1)
	for user in users:
	    a = 0
	    while a < int(_coupon_count):
	    	coupon = coffee_coupon(openid=user.openid,coffee_coupon_number=str(""+_coupon_price+""),user_coupon_validity_date=timezone.now() + datetime.timedelta(days=30))
            	coupon.save()
 		a += 1
	res["status"] = "ok"	
        return HttpResponse(json.dumps(res))
    except:
	res["status"] = "error"
        traceback.print_exc()
        return HttpResponse(json.dumps(res))
 

#个人中心 - 添加优惠券操作
@csrf_exempt
def add_coupon_operation(request):
    res = {}
    try:
    	data = request.POST
    	_coupon_price = data.get('coupon_price')
	coupon = Coupon(coupon_price=_coupon_price)
	coupon.save()
	res["status"] = "ok"	
        return HttpResponse(json.dumps(res))
    except:
	res["status"] = "error"
        traceback.print_exc()
        return HttpResponse(json.dumps(res))
   
#个人中心 - 编辑优惠券页面
def edit_coupon(request,id):
    try:
        if settings.TEST: 
    	    title = '编辑优惠券' 
    	    template = "edit_coupon.html"
	    coupon = Coupon.objects.filter(coupon_id=int(id))
            return render_to_response(template,{'title': title,'coupon':coupon,'coupon_id':id})
        else:
            if 'access_token' in request.session and 'openid' in request.session:
     	    	title = '编辑优惠券' 
    	    	template = "edit_coupon.html"
 	    	coupon = Coupon.objects.filter(coupon_id=int(id))
            	return render_to_response(template,{'title': title,'coupon':coupon,'coupon_id':id})
            else:
                url = 'https://open.weixin.qq.com/connect/oauth2/authorize?appid=%s&redirect_uri=%s&response_type=code&scope=snsapi_userinfo&state=1#wechat_redirect'%(config.appid, config.callback)
                return HttpResponseRedirect(url)
    except:
        traceback.print_exc()
        template = 'error.html'
        title = '获取数据失败'
        return render_to_response(template,{'title': title}) 

#个人中心 - 编辑优惠券操作
@csrf_exempt
def edit_coupon_operation(request):
    res = {}
    try:
    	data = request.POST
    	_coupon_price = data.get('coupon_price')
    	_coupon_id = data.get('coupon_id')
	Coupon.objects.filter(coupon_id=int(_coupon_id)).update(coupon_price=str(_coupon_price))
	res["status"] = "ok"	
        return HttpResponse(json.dumps(res))
    except:
	res["status"] = "error"
        traceback.print_exc()
        return HttpResponse(json.dumps(res))

#个人中心 - 删除优惠券操作
@csrf_exempt
def delete_coupon_operation(request):
    res = {}
    try:
    	data = request.POST
    	_coupon_id = data.get('coupon_id')
	Coupon.objects.filter(coupon_id=int(_coupon_id)).delete()
	res["status"] = "ok"	
        return HttpResponse(json.dumps(res))
    except:
	res["status"] = "error"
        traceback.print_exc()
        return HttpResponse(json.dumps(res))
 

#个人中心 - 优惠券设置
def coupon_setting(request):
    title = '优惠券设置'
    template = 'coupon_setting.html'
    try:
        if settings.TEST:
	    openid = 'o7go2597XriiWy4cgMWG_y3y7Bag'
	    template = 'coupon_setting.html'
	    user = User.objects.filter(openid=openid)[0]
	    coupons = Coupon.objects.all()
            return render_to_response(template,{'title': title,'user':user,'coupons':coupons}) 
        else:
            if 'access_token' in request.session and 'openid' in request.session:
                access_token = request.session["access_token"]
                if not access_token is None:
                    openid = request.session["openid"]  
            else:
                url = 'https://open.weixin.qq.com/connect/oauth2/authorize?appid=%s&redirect_uri=%s&response_type=code&scope=snsapi_userinfo&state=1#wechat_redirect'%(config.appid, config.callback)
                return HttpResponseRedirect(url)
    except:
        traceback.print_exc()
        template = 'error.html'
        title = '获取数据失败'
        return render_to_response(template,{'title': title}) 

          

#个人中心 - 邀请有礼
def invited_gift(request):
    title = '邀请有礼'
    template = 'invited_gift.html'
    try:
        if settings.TEST:
            return render_to_response(template,{'title': title}) 
        else:
            if 'access_token' in request.session and 'openid' in request.session:
                access_token = request.session["access_token"]
                if not access_token is None:
                    return render_to_response(template,{'title': title}) 
            else:
                url = 'https://open.weixin.qq.com/connect/oauth2/authorize?appid=%s&redirect_uri=%s&response_type=code&scope=snsapi_userinfo&state=1#wechat_redirect'%(config.appid, config.callback)
                return HttpResponseRedirect(url)
    except:
        traceback.print_exc()


#个人中心 - 关于我们
def about_us(request):
    title = '关于我们'
    template = 'about_us.html'
    try:
        if settings.TEST:
            return render_to_response(template,{'title': title}) 
        else:
            if 'access_token' in request.session and 'openid' in request.session:
                access_token = request.session["access_token"]
                if not access_token is None:
                    return render_to_response(template,{'title': title}) 
            else:
                url = 'https://open.weixin.qq.com/connect/oauth2/authorize?appid=%s&redirect_uri=%s&response_type=code&scope=snsapi_userinfo&state=1#wechat_redirect'%(config.appid, config.callback)
                return HttpResponseRedirect(url)
    except:
        traceback.print_exc()
        template = 'error.html'
        title = '获取数据失败'
        return render_to_response(template,{'title': title}) 



#存储购物车数据
@csrf_exempt
def store_cart_data(request):
    try:
        data = request.POST
        index = data.get('index')
        drinking_price = data.get('drinking_price')
        drinking_name = data.get('drinking_name')
        drinking_id = data.get('drinking_id')           
        index = int(index)
        drinking_price = float(drinking_price)
        #drinking_price = int(drinking_price[:-3])
        first_level_cart_info = {}
        second_level_cart_info = {}
        flag = 0  
        if 'access_token' in request.session and 'openid' in request.session:
            access_token = request.session["access_token"]
            if not access_token is None:
                #统计购买饮品信息
                if not "first_level_cart_info" in request.session:
                    first_level_cart_info['count'] = index
                    first_level_cart_info['price'] = ('%.2f' %drinking_price)
                    
                    tmp_second_level_cart_info = {}
                    tmp_second_level_cart_info['drinking_name'] = drinking_name
                    tmp_second_level_cart_info['drinking_price'] = ('%.2f' %drinking_price)
                    tmp_second_level_cart_info['drinking_count'] = index
                    tmp_second_level_cart_info['drinking_id'] = drinking_id
                    second_level_cart_info[drinking_id] = tmp_second_level_cart_info
                else:
                    #统计第一层级购物车信息
                    first_level_cart_info = request.session['first_level_cart_info']
                    count = first_level_cart_info['count']
                    first_level_cart_info['count'] = index + int(count)
                    price = first_level_cart_info['price']
                    first_level_cart_info['price'] = ('%.2f' % (drinking_price + float(price)))
                    #统计第二层级购物车信息
                    second_level_cart_info = request.session['second_level_cart_info']
                    #遍历第二层级购物车信息
                    for cart_info in second_level_cart_info.keys():
                        #判断已经存在的饮品名称和本次用户选择的饮品名称是否相同，相同则在原有基础上更改数目，否则统计session中若没有重复则添加新的饮品
                        if second_level_cart_info[cart_info]['drinking_name'] != drinking_name:
                            flag += 1
                            continue
                        else:
                            drink_count = second_level_cart_info[cart_info]['drinking_count']
                            second_level_cart_info[cart_info]['drinking_count'] = index + int(drink_count)

                    if int(flag) == len(second_level_cart_info):
                        new_cart_info = {}
                        new_cart_info['drinking_price'] = ('%.2f' %drinking_price)
                        new_cart_info['drinking_name'] = drinking_name
                        new_cart_info['drinking_count'] = index
                        new_cart_info['drinking_id'] = drinking_id
                        second_level_cart_info[drinking_id] = new_cart_info
                #每次操作购物车后存储session        
                request.session['first_level_cart_info'] = first_level_cart_info
                request.session['second_level_cart_info'] = second_level_cart_info
                res = {}
                res['status'] = "ok"
                res['first_level_cart_info'] = request.session['first_level_cart_info']
                res['second_level_cart_info'] =  request.session['second_level_cart_info']
                res = json.dumps(res)
                return HttpResponse(res)
        else:
            url = 'https://open.weixin.qq.com/connect/oauth2/authorize?appid=%s&redirect_uri=%s&response_type=code&scope=snsapi_userinfo&state=1#wechat_redirect'%(config.appid, config.callback)
            return HttpResponseRedirect(url)
    except:
        print traceback.print_exc()
        res['status'] = "error"
        res['first_level_cart_info'] = ""
        res['second_level_cart_info'] = ""
        return HttpResponse(res)

#删除购物车所有信息
def delete_cart_session(request):
    try:
        if 'access_token' in request.session and 'openid' in request.session:
            access_token = request.session["access_token"]
            if not access_token is None:
                del request.session['first_level_cart_info']
                del request.session['second_level_cart_info']
                return HttpResponse('ok')
        else:
            url = 'https://open.weixin.qq.com/connect/oauth2/authorize?appid=%s&redirect_uri=%s&response_type=code&scope=snsapi_userinfo&state=1#wechat_redirect'%(config.appid, config.callback)
            return HttpResponseRedirect(url)
    except:
        print traceback.print_exc()
        

#获取购物车信息
def get_cart_session(request):
    try:
        if 'access_token' in request.session and 'openid' in request.session:
            access_token = request.session["access_token"]
            if not access_token is None:
                res = {}
                res['first_level_cart_info'] = request.session['first_level_cart_info']
                res['second_level_cart_info'] =  request.session['second_level_cart_info']
                res = json.dumps(res)
                return HttpResponse(res)
        else:
            url = 'https://open.weixin.qq.com/connect/oauth2/authorize?appid=%s&redirect_uri=%s&response_type=code&scope=snsapi_userinfo&state=1#wechat_redirect'%(config.appid, config.callback)
            return HttpResponseRedirect(url)
    except:
        print traceback.print_exc()
    

#删除购物车饮品
@csrf_exempt
def delete_drinking(request):
    try:
        data = request.POST
        id = data.get('id')
        if 'access_token' in request.session and 'openid' in request.session:
            access_token = request.session["access_token"]
            if not access_token is None:
                flag = 0
                first_level_cart_info = request.session['first_level_cart_info']
                second_level_cart_info = request.session['second_level_cart_info']
                #遍历当前存储饮品字典key值为id的项，删除key和对应value
                length = len(second_level_cart_info)
                for drinking_id in second_level_cart_info.keys():
                    if int(drinking_id) == int(id):
                        #删除购物车最后一行，清空session
                        if length == 1:
                            delete_cart_session(request)                    
                            #构造数据返回页面
                            res = {}
                            res['status'] = 'last'
                            return HttpResponse(json.dumps(res))
                        else:
                            count = second_level_cart_info[drinking_id]['drinking_count']
                            price = second_level_cart_info[drinking_id]['drinking_price']
                            #统计某饮品总价
                            total_price = count * float(price)
                            #删除first_level_cart_info中对应的count和price值
                            temp1 = first_level_cart_info['count'] 
                            temp2 = first_level_cart_info['price']
                            first_level_cart_info['count'] = int(temp1) - int(count)
                            first_level_cart_info['price'] = ('%.2f' %(float(temp2) - float(total_price)))
                            #删除id对应k,v
                            second_level_cart_info.pop(drinking_id)
                            #修改完后存储session
                            request.session['first_level_cart_info'] = first_level_cart_info
                            request.session['second_level_cart_info'] = second_level_cart_info
                            #构造数据返回页面
                            res = {}
                            res['status'] = 'deleting'
                            res['drinking_id'] = id
                            res['total_price'] = first_level_cart_info['price']
                            res = json.dumps(res)
                            return HttpResponse(res)
        else:
            url = 'https://open.weixin.qq.com/connect/oauth2/authorize?appid=%s&redirect_uri=%s&response_type=code&scope=snsapi_userinfo&state=1#wechat_redirect'%(config.appid, config.callback)
            return HttpResponseRedirect(url)
    except:
        traceback.print_exc()

#修改购物车信息
@csrf_exempt
def modify_cart_data(request):
    try:
        data = request.POST
        drinking_count = data.get('drinking_count')
        drinking_id = data.get('drinking_id')
        modify_type = data.get('type')
        #level=1代表购买饮品时，到购物车时对饮品进行加减操作，level=2代表到结算页面时对饮品进行加减操作
        level = data.get('level')
        if 'access_token' in request.session and 'openid' in request.session:
            access_token = request.session["access_token"]
            if not access_token is None:
                coffee_info = coffee.objects.get(coffee_id=int(drinking_id))
                coffee_name = coffee_info.coffee_name
                coffee_price = coffee_info.coffee_price
                first_level_cart_info = request.session['first_level_cart_info']
                if int(modify_type) == 1:
                    if level == "l_1":
                        #first_level_cart_info数量减1,总价减去商品价格
                        first_level_cart_info['count'] = int(first_level_cart_info['count']) - 1
                        first_level_cart_info['price'] = ('%.2f' %(float(first_level_cart_info['price']) - float(coffee_price)))
                    else:
                        #
                        if int(first_level_cart_info['count']) != 1:
                            first_level_cart_info['count'] = int(first_level_cart_info['count']) - 1
                            first_level_cart_info['price'] = ('%.2f' %(float(first_level_cart_info['price']) - float(coffee_price)))
                else:
                    #first_level_cart_info数量加1,总价加上商品价格
                    first_level_cart_info['count'] = int(first_level_cart_info['count']) + 1
                    first_level_cart_info['price'] = ('%.2f' %(float(first_level_cart_info['price']) + float(coffee_price)))
                request.session['first_level_cart_info'] = first_level_cart_info
                
                #second_level_cart_info
                second_level_cart_info = request.session['second_level_cart_info']
                for cart_info in second_level_cart_info.keys():
                    if second_level_cart_info[cart_info]['drinking_id'] == drinking_id:
                        count = second_level_cart_info[cart_info]['drinking_count']
                        if int(modify_type) == 1:
                            #如果某饮品数量为0，则删掉此饮品数据，否则数量减1
                            if count == 1:
                                if level != "l_2":
                                    second_level_cart_info.pop(cart_info)
                            else:
                                second_level_cart_info[cart_info]['drinking_count'] = int(drinking_count) - 1
                        else:
                            second_level_cart_info[cart_info]['drinking_count'] = int(drinking_count) + 1
                        
                request.session['second_level_cart_info'] = second_level_cart_info
                res = {}
                res['status'] = "ok"
                res['first_level_cart_info'] = request.session['first_level_cart_info']
                res['second_level_cart_info'] =  request.session['second_level_cart_info']
                res = json.dumps(res)
                print "@@@@@res",res
                return HttpResponse(res)
        else:
            url = 'https://open.weixin.qq.com/connect/oauth2/authorize?appid=%s&redirect_uri=%s&response_type=code&scope=snsapi_userinfo&state=1#wechat_redirect'%(config.appid, config.callback)
            return HttpResponseRedirect(url)
    except:
        traceback.print_exc()
        res['status'] = "error"
        res['first_level_cart_info'] = ""
        res['second_level_cart_info'] = ""
        return HttpResponse(res)


#个人中心 - 查询具体某用户使用coupon情况
def coupon_detail(request,coupon_user=None):
    title = '用户券使用明细'
    template = 'dispatch_coupon.html'
    try:
        if settings.TEST:
	    openid = 'o7go2597XriiWy4cgMWG_y3y7Bag'
	    if coupon_user != 'no_coupon':
		#user
		user = User.objects.filter(openid=openid)[0]
		res = {}
		coupons = Coupon.objects.all()
		#user use coupon 
		coupon_user = User.objects.filter(phone_number=coupon_user)[0]
		print "@@@@@@@@@@@@@@2",coupon_user.openid
		user_coupon = []
		_coffee_coupons = coffee_coupon.objects.raw('select id,openid,coffee_coupon_number,count(*) as coupon_count,user_coupon_validity_date from coffee_coffee_coupon where openid="'+coupon_user.openid+'" group by coffee_coupon_number')	
		user_use_coupon = {}
		for _coffee_coupon in _coffee_coupons:
		   _user = User.objects.filter(openid=_coffee_coupon.openid)[0]
		   nick_name = _user.nickname
		   phone_number = _user.phone_number
		   coupon_price = _coffee_coupon.coffee_coupon_number
		   user_use_coupon[""+coupon_price+""] = _coffee_coupon.coupon_count
		   user_use_coupon["nickname"] = nick_name
		   user_use_coupon["phone_number"] = phone_number
		user_coupon.append(user_use_coupon)
		res["data"] = user_coupon
		return render_to_response(template,{'title': title,'user':user,'coupons':coupons,'results':json.dumps(res)})
	    else:
	 	#user
		user = User.objects.filter(openid=openid)[0]
		res = {}
		coupons = Coupon.objects.all()
		#user use coupon 
		users = User.objects.all()
		user_coupon = []
		for v_user in users:
		    _coffee_coupons = coffee_coupon.objects.raw('select id,openid,coffee_coupon_number,count(*) as coupon_count,user_coupon_validity_date from coffee_coffee_coupon where openid="'+v_user.openid+'" group by coffee_coupon_number')	
		    user_use_coupon = {}
		    for _coffee_coupon in _coffee_coupons:
	         	_user = User.objects.filter(openid=_coffee_coupon.openid)[0]
	         	nick_name = _user.nickname
	         	phone_number = _user.phone_number
	         	coupon_price = _coffee_coupon.coffee_coupon_number
	         	user_use_coupon[""+coupon_price+""] = _coffee_coupon.coupon_count
	         	user_use_coupon["nickname"] = nick_name
	         	user_use_coupon["phone_number"] = phone_number
		    user_coupon.append(user_use_coupon)
		res["data"] = user_coupon
		return render_to_response(template,{'title': title,'user':user,'coupons':coupons,'results':json.dumps(res)}) 
        else:
            if 'access_token' in request.session and 'openid' in request.session:
                access_token = request.session["access_token"]
                if not access_token is None:
                    openid = request.session["openid"]  
		    if coupon_user != 'no_coupon':
			#user
			user = User.objects.filter(openid=openid)[0]
			res = {}
			coupons = Coupon.objects.all()
			#user use coupon 
			user_coupon = []
			_coffee_coupons = coffee_coupon.objects.raw('select id,openid,coffee_coupon_number,count(*) as coupon_count,user_coupon_validity_date from coffee_coffee_coupon where openid="'+openid+'" group by coffee_coupon_number')	
			user_use_coupon = {}
			for _coffee_coupon in _coffee_coupons:
			   _user = User.objects.filter(openid=_coffee_coupon.openid)[0]
			   nick_name = _user.nickname
			   phone_number = _user.phone_number
			   coupon_price = _coffee_coupon.coffee_coupon_number
			   user_use_coupon[""+coupon_price+""] = _coffee_coupon.coupon_count
			   user_use_coupon["nickname"] = nick_name
			   user_use_coupon["phone_number"] = phone_number
			   user_coupon.append(user_use_coupon)
			res["data"] = user_coupon
			return render_to_response(template,{'title': title,'user':user,'coupons':coupons,'results':json.dumps(res)})
		    else:
			#user
			user = User.objects.filter(openid=openid)[0]
			res = {}
			coupons = Coupon.objects.all()
			#user use coupon 
			users = User.objects.all()
			user_coupon = []
			for v_user in users:
			    _coffee_coupons = coffee_coupon.objects.raw('select id,openid,coffee_coupon_number,count(*) as coupon_count,user_coupon_validity_date from coffee_coffee_coupon where openid="'+v_user.openid+'" group by coffee_coupon_number')	
			    user_use_coupon = {}
			    for _coffee_coupon in _coffee_coupons:
			        _user = User.objects.filter(openid=_coffee_coupon.openid)[0]
				nick_name = _user.nickname
				phone_number = _user.phone_number
				coupon_price = _coffee_coupon.coffee_coupon_number
				user_use_coupon[""+coupon_price+""] = _coffee_coupon.coupon_count
				user_use_coupon["nickname"] = nick_name
				user_use_coupon["phone_number"] = phone_number
			    user_coupon.append(user_use_coupon)
			res["data"] = user_coupon
			return render_to_response(template,{'title': title,'user':user,'coupons':coupons,'results':json.dumps(res)}) 
            else:
                url = 'https://open.weixin.qq.com/connect/oauth2/authorize?appid=%s&redirect_uri=%s&response_type=code&scope=snsapi_userinfo&state=1#wechat_redirect'%(config.appid, config.callback)
                return HttpResponseRedirect(url)
    except:
        traceback.print_exc()
        template = 'error.html'
        title = '获取数据失败'
        return render_to_response(template,{'title': title}) 






def balance_cart_stuff(request):
    try:
        first_level_cart_info = request.session['first_level_cart_info']
        second_level_cart_info = request.session['second_level_cart_info']
        res = {}
        res['first_level_cart_info'] = json.dumps(first_level_cart_info)
        res['second_level_cart_info'] = json.dumps(second_level_cart_info)
        #前端页面展示已购物div高度
        if len(second_level_cart_info) == 1:
            res['cart_info_height'] = 60
        else:
            res['cart_info_height'] = len(second_level_cart_info) * 70 - 10
        print "res",res
        template = 'shopping_cart.html' 
        title = "购物车结算"

        if settings.TEST:
            #优惠卷抵扣,判断是否有优惠卷
            openid = 'o7go2597XriiWy4cgMWG_y3y7Bag'
            coffee_coupon_temp = coffee_coupon.objects.raw('select count(*) as coupon_count,coffee_coupon_number,id from coffee_coffee_coupon where openid="o7go2597XriiWy4cgMWG_y3y7Bag" group by coffee_coupon_number')
            #组合为字典
            res_coupon_number = {}
            for coupon_temp in coffee_coupon_temp:
                res_coupon_number[int(coupon_temp.coffee_coupon_number)] = coupon_temp.coupon_count
            #判断当前剩余的最大面额，以及最大面额数量
            coupon_number_list = []
            for coupon_number in res_coupon_number.keys():
                coupon_number_list.append(coupon_number)
            #如果有优惠卷
            if coupon_number_list != []:
                coupon_number_max = max(coupon_number_list)
                if coupon_number_max in res_coupon_number.keys():
                    coupon_number_max_count = res_coupon_number[coupon_number_max]
                #确定优惠卷信息
                coffee_coupon_temp2 = coffee_coupon.objects.filter(openid=openid,coffee_coupon_number=coupon_number_max)[0]
                return render_to_response(template,{'title': title,'max_coupon': coffee_coupon_temp2,'result':res})
            else:
                return render_to_response(template,{'title': title,'max_coupon': "no_coupon",'result':res})
        else:
            if 'access_token' in request.session and 'openid' in request.session:
                access_token = request.session["access_token"]
                if not access_token is None:
                    #优惠卷抵扣,判断是否有优惠卷
                    openid = request.session['openid']
                    coffee_coupon_temp = coffee_coupon.objects.raw('select count(*) as coupon_count,coffee_coupon_number,id from coffee_coffee_coupon where openid="'+openid+'" group by coffee_coupon_number')
                    #组合为字典
                    res_coupon_number = {}
                    print "@@@@@@@@@@@@@@@@@@@coffee_coupon_temp@@@@@@@@@@@@@@@@@@@@@@@",coffee_coupon_temp
                    for coupon_temp in coffee_coupon_temp:
                        res_coupon_number[coupon_temp.coffee_coupon_number] = coupon_temp.coupon_count
                    #判断当前剩余的最大面额，以及最大面额数量
                    coupon_number_list = []
                    for coupon_number in res_coupon_number.keys():
                        coupon_number_list.append(coupon_number)
                     #如果有优惠卷
                    print "@@@@@@@@@@@@coupon_number_list",coupon_number_list
                    if coupon_number_list != []:
                        coupon_number_max = max(coupon_number_list)
                        if coupon_number_max in res_coupon_number.keys():
                            coupon_number_max_count = res_coupon_number[coupon_number_max]
                        #确定优惠卷信息
                        coffee_coupon_temp2 = coffee_coupon.objects.filter(openid=openid,coffee_coupon_number=coupon_number_max)[0]
                        return render_to_response(template,{'title': title,'max_coupon': coffee_coupon_temp2,'result':res})
                    else:
                        return render_to_response(template,{'title': title,'max_coupon': "no_coupon",'result':res})
            else:
                url = 'https://open.weixin.qq.com/connect/oauth2/authorize?appid=%s&redirect_uri=%s&response_type=code&scope=snsapi_userinfo&state=1#wechat_redirect'%(config.appid, config.callback)
                return HttpResponseRedirect(url)
    except:
        traceback.print_exc()


@csrf_exempt
def weixin_pay(request):
    try:
        if 'access_token' in request.session and 'openid' in request.session:
            access_token = request.session["access_token"]
            if not access_token is None:
                open_id = request.session['openid']
                body = params.MP_NAME
                trade_type = params.TRADE_TYPE
                #制作order_id
                rand = random.randint(100000, 999999)
		rand2 = random.randint(0000,8888)
                out_trade_no = '2019'+ str(rand2) + str(rand)
                
                #存order_id作为session，再存订单表时会用到
                request.session[open_id] = str(out_trade_no)
                data = request.POST
                #费用测试（1分）
                #total_fee = 1
                #线上运行
                total_fee = data.get('order_price')
                total_fee = float(total_fee) * 100
                
                spbill_create_ip = params.SPBILL_CREATE_IP
                notify_url = params.NOTIFY_URL
                order = WechatOrder(body=body,
                    trade_type = trade_type,
                    out_trade_no = out_trade_no,
                    openid = open_id,
                    total_fee = total_fee,
                    spbill_create_ip = spbill_create_ip,
                    notify_url = notify_url
                    )
                datas, error = order.order_post()
                import pprint
                pprint.pprint(datas)

                if error:
                    return HttpResponseServerError('get access_token error')
                order_data = datas['prepay_id'].encode('iso8859-1').decode('utf-8')
                pay = WechatPayAPI(package=order_data)
                dic = pay.get_dic()
                dic["package"] = "prepay_id=" + order_data
                return HttpResponse(json.dumps(dic), content_type="application/json")
        else:
            url = 'https://open.weixin.qq.com/connect/oauth2/authorize?appid=%s&redirect_uri=%s&response_type=code&scope=snsapi_userinfo&state=1#wechat_redirect'%(config.appid, config.callback)
            return HttpResponseRedirect(url)
    except:
        traceback.print_exc()



def weixin_pay_success(request,last_price,coupon_id):
    print "@@@@@@@@@@@@@@@@@it is coming@@@@@@@@@@@@@@@@@@@@@@@@@@@@@&&&&&&&&&&&&&&&&&&&&&"
    title = '支付成功页面'
    template = 'weixin_pay_success.html';
    try:
        if settings.TEST:
            #判断用户是否有刷新支付成功页面
            if 'second_level_cart_info' in request.session and 'first_level_cart_info' in request.session:
                #存trade表
                cart_info =  request.session['second_level_cart_info']
                open_id = 'o7go2597XriiWy4cgMWG_y3y7Bag'
                #遍历session中饮品信息，按次存放
                for cart in cart_info.keys():
                    a = 0
                    b = cart_info[cart]['drinking_count']
                    count = coffee_trade.objects.filter(openid=open_id,valid=1,coffee_id=cart_info[cart]['drinking_id'],flag=0).count()
                    #判断之前是否购买过咖啡，如果购买过，则将本次购买加入trade表
                    if int(count) > 0:
                        while a < int(b):
                            trade = coffee_trade(openid=open_id,valid=1,trade_date=timezone.now(),count=1,coffee_id=cart_info[cart]['drinking_id'])
                            trade.save()
                            coffee_temp = coffee.objects.get(coffee_id = cart_info[cart]['drinking_id'])
                            #如果还未领提取码，则不添加提取码信息至code表
                            coffee_code_count = coffee_code.objects.filter(openid=open_id,coffee_en_name=coffee_temp.coffee_en_name,type=1,coffee_id=cart_info[cart]['drinking_id']).count()
                            if coffee_code_count > 0:
                                extraction_code = random.sample('0123456789ABCDEF',8) 
                                extraction_code = ''.join(extraction_code)
                                coffee_code_temp = coffee_code(openid=open_id,coffee_en_name=coffee_temp.coffee_en_name,coffee_name=coffee_temp.coffee_name,coffee_code=extraction_code,coffee_code_id=coffee_temp.coffee_code,coffee_id=cart_info[cart]['drinking_id'],type=1)                          
                                coffee_code_temp.save()
                            a += 1
                    #如果之前未曾购买，则将本次购买加入trade表
                    elif int(count) == 0:
                        while a < int(b):
                            trade = coffee_trade(openid=open_id,valid=1,trade_date=timezone.now(),count=1,coffee_id=cart_info[cart]['drinking_id'])
                            trade.save()
                            a += 1
                
           
                #存订单表
                first_level_cart_info = request.session['first_level_cart_info']
                second_level_cart_info = request.session['second_level_cart_info']
                order_id = request.session[open_id]
                #判断是否有优惠券
                if coupon_id != "no_coupon":
                    #判断price的真实性
                    coupon_temp = coffee_coupon.objects.filter(id=coupon_id)[0]
                    price = str(first_level_cart_info['price'])
                    coupon_price = str(coupon_temp.coffee_coupon_number)
                    final_price = ('%.2f' %(float(price)-float(coupon_price)))
                    last_price = ('%.2f' %float(last_price))
                    if final_price == last_price:
                        coffee_order_temp = coffee_order(order_id=str(order_id),openid=open_id,trade_date=timezone.now(),total_fee=price,coffee_info=json.dumps(second_level_cart_info))     
                        coffee_order_temp.save()
                    else:
                        template = 'error.html'
                        title = '数据错误'
                        return render_to_response(template,{'title': title}) 

                    #删除用过的优惠卷
                    coffee_coupon.objects.filter(id=coupon_id).delete()
                else:
                    coffee_order_temp = coffee_order(order_id=str(order_id),openid=open_id,trade_date=timezone.now(),total_fee=first_level_cart_info['price'],coffee_info=json.dumps(second_level_cart_info))
                    coffee_order_temp.save()
                        


                #删除cart session
                del request.session['first_level_cart_info']
                del request.session['second_level_cart_info']
                
                return render_to_response(template,{'title': title}) 
            else:
                template = "error.html"
                title = "支付页面失败"
                msg = "请勿重复操作"
                return render_to_response(template,{'title': title,'message':msg}) 
                
        else:
            if 'access_token' in request.session and 'openid' in request.session:
                access_token = request.session["access_token"]
                if not access_token is None:
                    #判断用户是否有刷新支付成功页面
                    if 'second_level_cart_info' in request.session and 'first_level_cart_info' in request.session:
                        #存trade表
                        cart_info =  request.session['second_level_cart_info']
                        open_id = request.session['openid']
                        #遍历session中饮品信息，按次存放
                        for cart in cart_info.keys():
                            a = 0
                            b = cart_info[cart]['drinking_count']
                            res = judge_pacakge(cart_info[cart]['drinking_id'])
                            #套餐
                            print "@@@@@@@@@@@@@@@@@@@@@@@@@res.coffee_type@@@@@@@@@@@@@@@@@@@@@@@@@@",res['coffee_type']
                            if res['coffee_type'] == '3':
                                package_code = res['package_code']
                                package_code = package_code.split(',')
                                while a < int(b):
                                    for code in package_code:
                                        trade = coffee_trade(openid=open_id,valid=1,trade_date=timezone.now(),count=1,coffee_id=code)
                                        trade.save()
                                        coffee_temp = coffee.objects.get(coffee_id = int(code))
                                        #此处添加代码是因为如果用户已购买咖啡，如果用户已经获取提货码则需要在原有基础上添加至coffee_code表中
                                        coffee_code_count = coffee_code.objects.filter(openid=open_id,coffee_en_name=coffee_temp.coffee_en_name,type=1).count()
                                        if coffee_code_count > 0:
                                            extraction_code = random.sample('0123456789ABCDEF',8) 
                                            extraction_code = ''.join(extraction_code)
                                            coffee_code_temp = coffee_code(openid=open_id,coffee_en_name=coffee_temp.coffee_en_name,coffee_name=coffee_temp.coffee_name,coffee_code=extraction_code,coffee_code_id=coffee_temp.coffee_code,coffee_id=code,type=1)                          
                                            coffee_code_temp.save()
                                    a += 1


                            #茶饮单品或咖啡单品
                            else:
                                count = coffee_trade.objects.filter(openid=open_id,valid=1,coffee_id=cart_info[cart]['drinking_id'],flag=0).count()
                                print "@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@coffee_or_tea_count@@@@@@@@@@@@@@@@@@@@@",count
                                #判断之前是否购买过咖啡，如果购买过，则将本次购买加入trade表
                                if int(count) > 0:
                                    while a < int(b):
                                        trade = coffee_trade(openid=open_id,valid=1,trade_date=timezone.now(),count=1,coffee_id=cart_info[cart]['drinking_id'])
                                        trade.save()
                                        coffee_temp = coffee.objects.get(coffee_id = cart_info[cart]['drinking_id'])
                                        #如果还未领提取码，则不添加提取码信息至code表
                                        coffee_code_count = coffee_code.objects.filter(openid=open_id,coffee_en_name=coffee_temp.coffee_en_name,type=1).count()
                                        if coffee_code_count > 0:
                                            extraction_code = random.sample('0123456789ABCDEF',8) 
                                            extraction_code = ''.join(extraction_code)
                                            coffee_code_temp = coffee_code(openid=open_id,coffee_en_name=coffee_temp.coffee_en_name,coffee_name=coffee_temp.coffee_name,coffee_code=extraction_code,coffee_code_id=coffee_temp.coffee_code,coffee_id=cart_info[cart]['drinking_id'],type=1)                          
                                            coffee_code_temp.save()
                                        a += 1
                                #如果之前未曾购买，则将本次购买加入trade表
                                elif int(count) == 0:
                                    while a < int(b):
                                        trade = coffee_trade(openid=open_id,valid=1,trade_date=timezone.now(),count=1,coffee_id=cart_info[cart]['drinking_id'])
                                        trade.save()
                                        a += 1
                        
                   
                        #存订单表
                        first_level_cart_info = request.session['first_level_cart_info']
                        second_level_cart_info = request.session['second_level_cart_info']
                        order_id = request.session[open_id]
                        if coupon_id != "no_coupon":
                            #判断price的真实性
                            coupon_temp = coffee_coupon.objects.filter(id=coupon_id)[0]
                            price = str(first_level_cart_info['price'])
                            coupon_price = str(coupon_temp.coffee_coupon_number)
                            final_price = ('%.2f' %(float(price)-float(coupon_price)))
                            last_price = ('%.2f' %float(last_price))
                            print "**************final_price****************",final_price
                            print "**************last_price****************",last_price
                            if final_price == last_price:
                                coffee_order_temp = coffee_order(order_id=str(order_id),openid=open_id,trade_date=timezone.now(),total_fee=last_price,coffee_info=json.dumps(second_level_cart_info))     
                                coffee_order_temp.save()
                            else:
                                template = 'error.html'
                                title = '数据错误'
                                return render_to_response(template,{'title': title}) 

                            #删除使用过的优惠卷
                            coffee_coupon.objects.filter(id=coupon_id).delete()
                        else:
                            coffee_order_temp = coffee_order(order_id=str(order_id),openid=open_id,trade_date=timezone.now(),total_fee=str(first_level_cart_info['price']),coffee_info=json.dumps(second_level_cart_info))
                            coffee_order_temp.save()
                                


                        #删除cart session
                        del request.session['first_level_cart_info']
                        del request.session['second_level_cart_info']
                        
                        return render_to_response(template,{'title': title}) 
                    else:
                        template = "error.html"
                        title = "支付页面失败"
                        msg = "请勿重复操作"
                        return render_to_response(template,{'title': title,'message':msg}) 
                        
            else:
                url = 'https://open.weixin.qq.com/connect/oauth2/authorize?appid=%s&redirect_uri=%s&response_type=code&scope=snsapi_userinfo&state=1#wechat_redirect'%(config.appid, config.callback)
                return HttpResponseRedirect(url)
    except:
        traceback.print_exc()

       

def weixin_pay_failure(request):
    title = '支付失败页面'
    template = 'weixin_pay_failure.html';
    if 'access_token' in request.session and 'openid' in request.session:
        access_token = request.session["access_token"]
        if not access_token is None:
            return render_to_response(template,{'title': title}) 
    else:
        url = 'https://open.weixin.qq.com/connect/oauth2/authorize?appid=%s&redirect_uri=%s&response_type=code&scope=snsapi_userinfo&state=1#wechat_redirect'%(config.appid, config.callback)
        return HttpResponseRedirect(url)



#饮品数量减至0，返回空白页提醒用户未选购咖啡，并跳回选购页面
def temp_0(request):
    template = 'temp_0.html' 
    title = "购物车结算"
    if 'access_token' in request.session and 'openid' in request.session:
        access_token = request.session["access_token"]
        if not access_token is None:
            return render_to_response(template,{'title':title})
    else:
        url = 'https://open.weixin.qq.com/connect/oauth2/authorize?appid=%s&redirect_uri=%s&response_type=code&scope=snsapi_userinfo&state=1#wechat_redirect'%(config.appid, config.callback)
        return HttpResponseRedirect(url)



    
#查看提货码
@csrf_exempt
def get_code(request,coffee_id,coffee_count,type):
    title = '查看提货码'
    template = 'extraction_code.html'
    try:
        if settings.TEST:
            openid_temp = 'o7go2597XriiWy4cgMWG_y3y7Bag'
            coffee_temp = coffee.objects.get(coffee_id=coffee_id)
            #type=1为我的咖啡卷，type=2为我的优惠卷
            if int(type) == 1:
                coffee_info = coffee_code.objects.filter(openid=openid_temp,coffee_en_name=coffee_temp.coffee_en_name,type=1)
            else:
                coffee_info = coffee_code.objects.filter(openid=openid_temp,coffee_en_name=coffee_temp.coffee_en_name,type=2)
            return render_to_response(template,{'title': title,'coffee_info':coffee_info,'coffee_count':coffee_count,'coffee_name':coffee_temp.coffee_name}) 
        else:
            if 'access_token' in request.session and 'openid' in request.session:
                access_token = request.session["access_token"]
                if not access_token is None:
                    openid_temp = request.session["openid"]
                    coffee_temp = coffee.objects.get(coffee_id=coffee_id)
                    coffee_en_name = coffee_temp.coffee_en_name
                    coffee_name = coffee_temp.coffee_name
                    if int(type) == 1:
                        coffee_info = coffee_code.objects.filter(openid=openid_temp,coffee_en_name=coffee_temp.coffee_en_name,type=1)
                    else:
                        coffee_info = coffee_code.objects.filter(openid=openid_temp,coffee_en_name=coffee_temp.coffee_en_name,type=2)
                    return render_to_response(template,{'title': title,'coffee_info':coffee_info,'coffee_count':coffee_count,'coffee_name':coffee_temp.coffee_name}) 
            else:
                url = 'https://open.weixin.qq.com/connect/oauth2/authorize?appid=%s&redirect_uri=%s&response_type=code&scope=snsapi_userinfo&state=1#wechat_redirect'%(config.appid, config.callback)
                return HttpResponseRedirect(url)
    except:
        traceback.print_exc()

 
            
 


#生成提货码
@csrf_exempt
def generate_extraction_code(request,coffee_id,coffee_count,type):
    title = '获取提货码'
    template = 'extraction_code.html'
    try:
        if settings.TEST:
            openid_temp = 'o7go2597XriiWy4cgMWG_y3y7Bag'    
            coffee_temp = coffee.objects.get(coffee_id=coffee_id)
            coffee_en_name = coffee_temp.coffee_en_name
            coffee_name = coffee_temp.coffee_name
            coffee_coding = coffee_temp.coffee_code
            count = 0
            #判断是否已生成过提货码
            #1代表我的咖啡卷，2代表我的优惠卷中的饮品卷
            if int(type) == 1:
                coffee_code_count = coffee_code.objects.filter(openid=openid_temp,coffee_en_name=coffee_en_name,type=1).count()
            else:
                coffee_code_count = coffee_code.objects.filter(openid=openid_temp,coffee_en_name=coffee_en_name,type=2).count()
            if int(coffee_code_count) == int(coffee_count):
                template = "error.html"
                title = "获取提货码错误"
                msg = "请勿重复操作"
                return render_to_response(template,{'title': title,'message':msg}) 
            else:
                #生成提货码
                while count < int(coffee_count):
                    extraction_code = random.sample('0123456789ABCDEF',8)
                    extraction_code = ''.join(extraction_code)
                    if int(type) == 1:
                        coffee_code_temp = coffee_code(openid=openid_temp,coffee_en_name=coffee_en_name,coffee_name=coffee_name,coffee_code=extraction_code,coffee_code_id=coffee_coding,coffee_id=coffee_id) 
                    else:
                        coffee_code_temp = coffee_code(openid=openid_temp,coffee_en_name=coffee_en_name,coffee_name=coffee_name,coffee_code=extraction_code,coffee_code_id=coffee_coding,coffee_id=coffee_id,type=2) 
                    coffee_code_temp.save()
                    count +=1
                #查出此openid，coffee_id 下购买的提取码
                if int(type) == 1:
                    coffee_info = coffee_code.objects.filter(openid=openid_temp,coffee_en_name=coffee_en_name,type=1)
                else:
                    coffee_info = coffee_code.objects.filter(openid=openid_temp,coffee_en_name=coffee_en_name,type=2)
                return render_to_response(template,{'title': title,'coffee_info':coffee_info,'coffee_count':coffee_count,'coffee_name':coffee_name}) 
        else:
            if 'access_token' in request.session and 'openid' in request.session:
                access_token = request.session["access_token"]
                if not access_token is None:
                    openid_temp = request.session["openid"]
                    coffee_temp = coffee.objects.get(coffee_id=coffee_id)
                    coffee_en_name = coffee_temp.coffee_en_name
                    coffee_name = coffee_temp.coffee_name
                    coffee_coding = coffee_temp.coffee_code
                    count = 0
                    #判断是否已生成过提货码
                    #1代表我的咖啡卷，2代表我的优惠卷中的饮品卷
                    if int(type) == 1:
                        coffee_code_count = coffee_code.objects.filter(openid=openid_temp,coffee_en_name=coffee_en_name,type=1).count()
                    else:
                        coffee_code_count = coffee_code.objects.filter(openid=openid_temp,coffee_en_name=coffee_en_name,type=2).count()
                    if int(coffee_code_count) == int(coffee_count):
                        template = "error.html"
                        title = "获取提货码错误"
                        msg = "请勿重复操作"
                        return render_to_response(template,{'title': title,'message':msg}) 
                    else:
                        #生成提货码
                        while count < int(coffee_count):
                            extraction_code = random.sample('0123456789ABCDEF',8)
                            extraction_code = ''.join(extraction_code)
                            if int(type) == 1:
                                coffee_code_temp = coffee_code(openid=openid_temp,coffee_en_name=coffee_en_name,coffee_name=coffee_name,coffee_code=extraction_code,coffee_code_id=coffee_coding,coffee_id=coffee_id) 
                            else:
                                coffee_code_temp = coffee_code(openid=openid_temp,coffee_en_name=coffee_en_name,coffee_name=coffee_name,coffee_code=extraction_code,coffee_code_id=coffee_coding,coffee_id=coffee_id,type=2) 
                            coffee_code_temp.save()
                            count +=1
                        #查出此openid，coffee_id 下购买的提取码
                        if int(type) == 1:
                            coffee_info = coffee_code.objects.filter(openid=openid_temp,coffee_en_name=coffee_en_name,type=1)
                        else:
                            coffee_info = coffee_code.objects.filter(openid=openid_temp,coffee_en_name=coffee_en_name,type=2)
                        return render_to_response(template,{'title': title,'coffee_info':coffee_info,'coffee_count':coffee_count,'coffee_name':coffee_name}) 
            else:
                url = 'https://open.weixin.qq.com/connect/oauth2/authorize?appid=%s&redirect_uri=%s&response_type=code&scope=snsapi_userinfo&state=1#wechat_redirect'%(config.appid, config.callback)
                return HttpResponseRedirect(url)
    except:
        traceback.print_exc()

           
def judge_pacakge(drinking_id):
    coffee_temp = coffee.objects.filter(coffee_id=drinking_id)[0]
    coffee_type_temp = coffee_temp.coffee_type
    res = {}
    res['coffee_type'] = coffee_type_temp
    #套餐类型为3
    if str(coffee_type_temp) == '3':
        package_code_temp = coffee_temp.package_code
        res['package_code'] = str(package_code_temp)
    else:
        coffee_code_temp = coffee_temp.coffee_code
        res['coffee_code'] = str(coffee_code_temp)
    return res
