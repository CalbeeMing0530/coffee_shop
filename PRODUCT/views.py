# -*- coding: utf-8 -*-  
from django.shortcuts import render
import sys
import time,datetime
import json
import traceback

from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
                         
from django.views.generic import TemplateView
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render
from django.http import HttpResponse
from django.conf import settings
from django.core.exceptions import * 
from django.db.models import Q 

from coffee.models import coffee_code,coffee_trade
# Create your views here.

class PRODUCT(generics.RetrieveUpdateDestroyAPIView):
    def post(self,request):
        try:
            ID = request.GET["ID"]
            VMC = request.GET["VMC"]
            PID = request.GET["PID"]
            MAC = request.GET["MAC"]
            print "@@@@@@@@@@@@@@INFO",ID,VMC,PID,MAC
            #判断coffee_code表中是否有此提货码信息
            print "@@@@@@@@@@@@@str(ID)",str(ID)
            coffee_code_count = coffee_code.objects.filter(coffee_code_order_id=str(ID)).count()
            if coffee_code_count == 1:
                coffee_code_temp = coffee_code.objects.filter(coffee_code_order_id=str(ID))[0]
                coffee_code_v1 = coffee_code_temp.coffee_code
                openid = coffee_code_temp.openid
                coffee_id = coffee_code_temp.coffee_id
                #删除code表中数据
                coffee_code.objects.filter(coffee_code=coffee_code_v1).delete()
                #删除trade表数据
                coffee_trade_temp = coffee_trade.objects.filter(openid=openid,coffee_id=coffee_id)[0].delete() 
            res = {}
            res['code'] = 200
            res = json.dumps(res)
            return HttpResponse(res)
        except:
            traceback.print_exc()




