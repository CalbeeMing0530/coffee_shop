# -*- coding: utf-8 -*-
# ----------------------------------------------
# @Time    : 19-4-2
# @Author  : puming
# @File    : WechatAPI.py
# @CopyRight: puming
# ----------------------------------------------
import hashlib
import random
import time
from xml.etree.ElementTree import fromstring

import requests

import config

class WechatAPI(object):
    def __init__(self):
        self.config = config
        #self._access_token = None
        #self._openid = None
        self.dic = {}


    def process_response_pay(self, rsp):
        """解析微信支付下单返回的json数据，返回相对应的dict, 错误信息"""
        rsp = self.xml_to_array(rsp)
        print "@@@@@@@@@@@@@@rwsp",rsp
        if 'SUCCESS' != rsp['return_code']:
            return None, {'code': '9999', 'msg': rsp['return_msg']}
        if 'prepay_id' in rsp:
            return {'prepay_id': rsp['prepay_id']}, None

        return rsp, None

    @staticmethod
    def create_time_stamp():
        """产生时间戳"""
        now = time.time()
        return int(now)

    @staticmethod
    def create_nonce_str(length=32):
        """产生随机字符串，不长于32位"""
        chars = "abcdefghijklmnopqrstuvwxyz0123456789"
        strs = []
        for x in range(length):
            strs.append(chars[random.randrange(0, len(chars))])
        return "".join(strs)

    @staticmethod
    def xml_to_array(xml):
        """将xml转为array"""
        array_data = {}
        root = fromstring(xml)
        for child in root:
            value = child.text
            array_data[child.tag] = value
        return array_data

    def get_sign(self):
        """生成签名"""
        # 签名步骤一：按字典序排序参数
        key = sorted(self.dic.keys())
        buffer = []
        for k in key:
            buffer.append("{0}={1}".format(k, self.dic[k]))
        # self.dic["paySign"] = self.get_sign(jsApiObj)

        parm = "&".join(buffer)
        # 签名步骤二：在string后加入KEY
        parm = "{0}&key={1}".format(parm, self.config.api_key).encode('utf-8')
        # 签名步骤三：MD5加密
        signature = hashlib.md5(parm).hexdigest()
        # 签名步骤四：所有字符转为大写
        result_ = signature.upper()
        return result_

    def array_to_xml(self, sign_name=None):
        """array转xml"""
        if sign_name is not None:
            self.dic[sign_name] = self.get_sign()
        xml = ["<xml>"]
        for k in self.dic.keys():
            xml.append("<{0}>{1}</{0}>".format(k, self.dic[k]))
        xml.append("</xml>")
        return "".join(xml)



class WechatPayAPI(WechatAPI):
    def __init__(self, package, sign_type=None):
        #super().__init__()
        self.config = config
        self.appId = self.config.appid
        self.timeStamp = self.create_time_stamp()
        self.nonceStr = self.create_nonce_str()
        self.package = package
        self.signType = sign_type
        self.dic = {"appId": self.config.appid, "timeStamp": "{0}".format(self.create_time_stamp()),
                    "nonceStr": self.create_nonce_str(), "package": "prepay_id={0}".format(self.package)}
        if sign_type is not None:
            self.dic["signType"] = sign_type
        else:
            self.dic["signType"] = "MD5"

    def get_dic(self):
        self.dic['paySign'] = self.get_sign()
        return self.dic


class WechatOrder(WechatAPI):
    def __init__(self, body, trade_type, out_trade_no, total_fee, spbill_create_ip, notify_url, device_info=None,
                 sign_type=None, attach=None, fee_type=None, time_start=None, time_expire=None, goods_tag=None,
                 product_id=None, detail=None, limit_pay=None, openid=None, scene_info=None):
        #super().__init__()
        self.device_info = device_info  
        self.nonce_str = self.create_nonce_str()
        self.sign_type = sign_type  
        self.detail = detail  
        self.body = body
        self.attach = attach  
        self.out_trade_no = out_trade_no
        self.fee_type = fee_type  
        self.total_fee = int(total_fee)
        self.spbill_create_ip = spbill_create_ip
        self.time_start = time_start  
        self.time_expire = time_expire  
        self.goods_tag = goods_tag  
        self.notify_url = notify_url
        self.trade_type = trade_type
        self.product_id = product_id  
        self.limit_pay = limit_pay  
        self.openid = openid  
        self.scene_info = scene_info  
        self.config = config
        self.dic = {
                    "appid": self.config.appid, 
                    "mch_id": self.config.mch_id,
                    "nonce_str": self.nonce_str, "body": self.body,
                    'out_trade_no': out_trade_no,
                    'openid': self.openid,
                    "total_fee": self.total_fee, 
                    "spbill_create_ip": self.spbill_create_ip,
                    "notify_url": self.notify_url,
                    "trade_type": self.trade_type
        }
        if self.device_info is not None:
            self.dic["device_info"] = self.device_info
        if self.sign_type is not None:
            self.dic["sign_type"] = self.sign_type
        if self.detail is not None:
            self.dic["detail"] = self.detail
        if self.attach is not None:
            self.dic["attach"] = self.attach
        if self.fee_type is not None:
            self.dic["fee_type"] = self.fee_type
        if self.time_start is not None:
            self.dic["time_start"] = self.time_start
        if self.time_expire is not None:
            self.dic["time_expire"] = self.time_expire
        if self.goods_tag is not None:
            self.dic["goods_tag"] = self.goods_tag
        if self.product_id is not None:
            self.dic["product_id"] = self.product_id
        if self.limit_pay is not None:
            self.dic["limit_pay"] = self.limit_pay
        if self.openid is not None:
            self.dic["openid"] = self.openid
        if self.scene_info is not None:
            self.dic["scene_info"] = self.scene_info

    def order_post(self):
        if self.config.appid is None:
            return None, True
        xml_ = self.array_to_xml('sign')
        import pprint
        pprint.pprint(xml_)
        data = requests.post(self.config.order_url, data=xml_.encode('utf-8'),
                             headers={'Content-Type': 'text/xml'})
        return self.process_response_pay(data.content)
