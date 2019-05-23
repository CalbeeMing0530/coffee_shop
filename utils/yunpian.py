# -*- coding: utf-8 -*-  
import requests
import httplib
import urllib
import json

class YunPian(object):
    def __init__(self,api_key):
        self.api_key = api_key
        self.single_send_url='https://sms.yunpian.com/v2/sms/single_send.json'

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

if __name__=='__main__':
    yun_pian = YunPian('***************（你的apikey）')
    yun_pian.send_sms('***（验证码）','*******（手机号）')
