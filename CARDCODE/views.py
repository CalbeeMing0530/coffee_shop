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


from utils import http_utils
from coffee.models import coffee,coffee_code,coffee_trade


import hashlib
from config import params
# Create your views here.

class CARDCODE(generics.RetrieveUpdateDestroyAPIView):
    def post(self,request):
        try:
            ID = request.GET['ID']
            VMC = request.GET['VMC']
            PID = request.GET['PID']
            CODE = request.GET['CODE']
            MAC = request.GET['MAC']
            print "info*******************************",ID,VMC,PID,CODE,MAC
            res = {}
            #验证逻辑
            coffee_code_count = coffee_code.objects.filter(coffee_code=CODE).count()
            if coffee_code_count > 0:
                coffee_code_temp = coffee_code.objects.filter(coffee_code=CODE)[0]
                PID = coffee_code_temp.coffee_code_id
                vcoffee_id = coffee_code_temp.coffee_id
                openid = coffee_code_temp.openid
                coffee_temp = coffee.objects.filter(coffee_id=vcoffee_id)[0]
                print "@@@@@coffee_temp@@@@@",coffee_temp.coffee_concentration
                res['resultCode'] = 1
                #制作咖啡
                temp_str = "ID="+str(ID)+"&USERNAME=zhongming&PASSWORD=84296BA75491CBC5&VMC="+str(VMC)+"&PTYPE=FASTCODE&PID="+str(PID)+"&FASTCODE="+str(coffee_temp.coffee_concentration)+""
                m = hashlib.md5()
                m.update(temp_str)
                md5_str = m.hexdigest()
                final_str = "/FASTCODE?ID="+str(ID)+"&USERNAME=zhongming&VMC="+str(VMC)+"&PTYPE=FASTCODE&PID="+str(PID)+"&FASTCODE="+str(coffee_temp.coffee_concentration)+"&MAC="+str(md5_str)+""
                url = params.VENDOR_URL + final_str
                r = http_utils.send_request(url = url, method= 'GET') 
                vres = json.dumps(r.json())
                vres = json.loads(vres)
                if vres['status'] == "success":
                    #开始制作中。。。。。
                    coffee_code.objects.filter(coffee_code=CODE).update(coffee_code_order_id=str(ID))
                else:
                    print "vres",vres['message']
            else:
                res['resultCode'] = 0
                res['reason'] = '提货码不存在，请重新输入'
            res = json.dumps(res)
            return HttpResponse(res)
        except:
            traceback.print_exc()




