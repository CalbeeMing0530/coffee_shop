# -*- coding: utf-8 -*-
import config
from utils import http_utils
import traceback

base_url = 'https://api.weixin.qq.com'
#获取用户信息accesstoken
def get_access_token(code):
    global base_url
    url = base_url + '/sns/oauth2/access_token?appid=%s&secret=%s&code=%s&grant_type=authorization_code'%(config.appid,config.appsecret,code)
    r = http_utils.send_request(url = url, method= 'GET')
    return r.json()

#获取基础支持access_token
def get_base_access_token():
    global base_url
    url = base_url + '/cgi-bin/token?grant_type=client_credential&appid=%s&secret=%s'%(config.appid,config.appsecret)
    r = http_utils.send_request(url = url, method= 'GET')
    print '-------------------r.json',r.json
    return r.json()


#获取用户基本信息
def get_user_info(access_token, openid):
    global base_url
    url = base_url + '/sns/userinfo?access_token=%s&openid=%s&lang=zh_CN'%(access_token,openid) 
    r = http_utils.send_request(url = url, method= 'GET')
    return r.json()


