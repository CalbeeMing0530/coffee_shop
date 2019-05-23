# -*- coding: utf-8 -*-  
from django.shortcuts import render
import sys
import time,datetime
import json
import traceback
import config
import hashlib

from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
from bs4 import BeautifulSoup
                         
from django.views.generic import TemplateView
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render
from django.http import HttpResponse
from django.conf import settings
from django.core.exceptions import * 
from django.db.models import Q 
from coffee.models import coffee_order

# Create your views here.

class WEIXIN_PAY(generics.RetrieveUpdateDestroyAPIView):
    def post(self,request):
        try:
            print "@@@@@@@@@@@@@@@@@@",request.body
            data_dict = trans_xml_to_dict(request.body)
            print '支付回调结果', data_dict
            sign = data_dict.pop('sign')
            out_trade_no = data_dict.get('out_trade_no','')
            open_id = data_dict.get('openid','')
            print "@@@@@@@@@@@@@@@out_trade_no@@@@@@@@@@@@@",out_trade_no
            print "@@@@@@@@@@@@@@@openid@@@@@@@@@@@@@",open_id
            print "@@@@@@@@@@@@@@@sign",sign
            back_sign = get_sign(data_dict, config.api_key)
            print "@@@@@@@@@@back_sign",back_sign
            # 验证签名是否与回调签名相同
            if sign == back_sign and data_dict['return_code'] == 'SUCCESS':
                '''
                检查对应业务数据的状态，判断该通知是否已经处理过，如果没有处理过再进行处理，如果处理过直接返回结果成功。
                '''
                count = coffee_order.objects.filter(order_id=str(out_trade_no)).count()
                print "@@@@@@@@@@@@@@@count",count
                if int(count) > 0:
                    coffee_order_temp = coffee_order.objects.filter(order_id=str(out_trade_no))[0]
                    print "@@@@@@@@@@@valid",coffee_order_temp.valid
                    if int(coffee_order_temp.valid) == 0:
                        coffee_order.objects.filter(order_id=str(out_trade_no)).update(valid=1)
                        #此部分openid session暂时保留，不会占用太多内存空间(因为目前还不知再哪出删除此session较为合适)
                        #open_id = str(open_id)
                        #del request.session[open_id]
                    return HttpResponse(trans_dict_to_xml({'return_code': 'SUCCESS', 'return_msg': 'OK'}))
                else:
                    #用户还未点击成功支付页面按钮，所以未存库，此种情况忽略
                    return HttpResponse(trans_dict_to_xml({'return_code': 'FAIL', 'return_msg': 'error'}))
            else:
                return HttpResponse(trans_dict_to_xml({'return_code': 'FAIL', 'return_msg': 'SIGNERROR'}))
        except:
            traceback.print_exc()
            return HttpResponse(trans_dict_to_xml({'return_code': 'FAIL', 'return_msg': 'error'}))


def trans_xml_to_dict(data_xml):
    soup = BeautifulSoup(data_xml, features='xml')
    xml = soup.find('xml')  # 解析XML
    if not xml:
        return {}
    data_dict = dict([(item.name, item.text) for item in xml.find_all()])
    return data_dict


def get_sign(data_dict, key):
    # 签名函数，参数为签名的数据和密钥
    params_list = sorted(data_dict.items(), key=lambda e: e[0], reverse=False)  # 参数字典倒排序为列表
    params_str = "&".join(u"{}={}".format(k, v) for k, v in params_list) + '&key=' + key
    # 组织参数字符串并在末尾添加商户交易密钥
    md5 = hashlib.md5()  # 使用MD5加密模式
    md5.update(params_str.encode('utf-8'))  # 将参数字符串传入
    sign = md5.hexdigest().upper()  # 完成加密并转为大写
    return sign



def trans_dict_to_xml(data_dict):
    xml = ["<xml>"]
    for k in data_dict.keys():
        xml.append("<{0}>{1}</{0}>".format(k, data_dict[k]))
    xml.append("</xml>")
    return "".join(xml)


