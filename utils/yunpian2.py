# -*- coding: utf-8 -*-  
import requests
import httplib
import urllib
import json

class YunPian(object):
    def __init__(self,api_key):
        self.api_key = api_key
        self.single_send_url='https://sms.yunpian.com/v2/sms/single_send.json'
	self.batch_send = 'https://sms.yunpian.com/v2/sms/batch_send.json'
    
    def send_sms(self,code,mobile):
        parmas = {
            'apikey':self.api_key,
            'text':'【咖啡N次方】您的验证码是'+code+'，5分钟内有效，请您尽快验证，感谢您的使用。',
            'mobile': mobile
        }
        params = urllib.urlencode(parmas)
        headers = {
            "Content-type": "application/x-www-form-urlencoded",
            "Accept": "text/plain"
        }
        conn = httplib.HTTPSConnection('sms.yunpian.com', port=443, timeout=30)
        conn.request("POST", self.single_send_url, params, headers)
        response = conn.getresponse()
        response_str = response.read()
        conn.close()
        res = json.loads(response_str)
        msg = res['msg']
        return msg
    
    def send_coupon_sms(self,money,number,mobile):
        try:
            money = str(('%.0f' % float(money)))
            number = str(number)
            conn = httplib.HTTPSConnection('sms.yunpian.com', port=443, timeout=30)
            params = {
             'apikey':self.api_key,
             'mobile': mobile,
	         'text':'【咖啡N次方】已给您的咖啡账户存入'+money+'元抵扣券'+number+'张，去喝一杯吧！马上去公众号商城购买咖啡/奶茶，不限时领取。回T退订'
            }
            params = urllib.urlencode(params)
            headers = {
             	"Content-type": "application/x-www-form-urlencoded;charset=utf-8",
             	"Accept": "application/json;charset=utf-8"
            }
            conn.request("POST", self.batch_send, params,headers)
            response = conn.getresponse()
            response_str = response.read()
            res = json.loads(response_str)
            conn.close()
            return res
        except:
            import traceback
            traceback.print_exc()    

if __name__=='__main__':
    yun_pian = YunPian('***************（你的apikey）')
    yun_pian.send_sms('***（验证码）','*******（手机号）')
