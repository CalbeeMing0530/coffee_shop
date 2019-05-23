# -*- coding: utf-8 -*-  
from django.shortcuts import render
from config import conf 
import config
import json
from django.http import HttpResponse
from wechat_sdk import WechatBasic
from wechat_sdk.messages import *
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponseRedirect
from utils.common import ierror
from utils.common.WXBizMsgCrypt import * 
from users.models import User
from utils import wechat
from utils import http_utils
import hashlib
import traceback


@csrf_exempt
def callback(request):
    #import pdb
    #pdb.set_trace()
    try:
        response = ""
        if request.method == 'GET':
            signature = request.GET['signature']
            timestamp = request.GET['timestamp']
            nonce = request.GET['nonce']
            echostr = request.GET['echostr']
            list = [conf.token, timestamp, nonce]
            list.sort()
            sha1 = hashlib.sha1()
            map(sha1.update, list)
            hashcode = sha1.hexdigest()
            print "handle/GET func: hashcode, signature: ", hashcode, signature
            if hashcode == signature:
                response = echostr
            else:
                response = ""
            return HttpResponse(response)
        elif request.method == 'POST':
            signature = request.GET['signature']
            timestamp = request.GET['timestamp']
            nonce = request.GET['nonce']
            openid = request.GET['openid']
            list = [conf.token, timestamp, nonce]
            list.sort()
            sha1 = hashlib.sha1()
            map(sha1.update, list)
            hashcode = sha1.hexdigest()
            print "handle/GET func: hashcode, signature: ", hashcode, signature
            req_data = request.body
            if hashcode == signature:
                xml_tree = ET.fromstring(req_data)
                type = xml_tree.find("MsgType").text
                xml_tree = ET.fromstring(req_data)
                to_name = xml_tree.find("ToUserName").text
                from_name = xml_tree.find("FromUserName").text
                time = xml_tree.find("CreateTime").text
                type = xml_tree.find("MsgType").text
                print "--------------type",type
                print '--------------time',time
                print '--------------from_name',from_name
                print '---------------to_name--------',to_name
                print '---------------req_data--------',req_data
                if type == "event":
                    if not xml_tree.find("Event") is None:
                        Event = xml_tree.find("Event").text
                        #关注/取消公众号事件
                        if Event == "subscribe":
                                content = config.content
                                response = "<xml><ToUserName><![CDATA[%s]]></ToUserName><FromUserName><![CDATA[%s]]></FromUserName><CreateTime>1348831860</CreateTime><MsgType><![CDATA[text]]></MsgType><Content><![CDATA[%s]]></Content><MsgId>1234567890123456</MsgId></xml>"%(from_name, to_name, content)
                                print "subscribe"
                        elif Event == "unsubscribe":
                            print "unsubscribe"
                        return HttpResponse(response)
                elif type == "text":
                    content = xml_tree.find("Content").text
                    content = content.encode('utf-8')
                    re_content = content
                    response = "<xml><ToUserName><![CDATA[%s]]></ToUserName><FromUserName><![CDATA[%s]]></FromUserName><CreateTime>1348831860</CreateTime><MsgType><![CDATA[text]]></MsgType><Content><![CDATA[%s]]></Content><MsgId>1234567890123456</MsgId></xml>"%(from_name, to_name, config.re_content)
                    return HttpResponse(response)
                else:
                    return HttpResponse("")
                
    except:
        traceback.print_exc()        

def handle_message(message, wechat):
    id = message.id          # 对应于 XML 中的 MsgId
    target = message.target  # 对应于 XML 中的 ToUserName
    source = message.source  # 对应于 XML 中的 FromUserName
    time = message.time      # 对应于 XML 中的 CreateTime
    type = message.type      # 对应于 XML 中的 MsgType
    resp = ""
    content = ""
    if isinstance(message, TextMessage):
        content = message.content 
        resp = content
    elif isinstance(message, ImageMessage):
        picurl = message.picurl
        media_id = message.media_id
        content = picurl
        resp = "good draw"
    elif isinstance(message, VoiceMessage):
        media_id = message.media_id
        recognition = message.recognition
        content = recognition
        resp = "right?" 
    elif isinstance(message, VideoMessage) or isinstance(message, ShortVideoMessage):
        media_id = message.media_id
        thumb_media_id = message.thumb_media_id
        resp = "media_id %s, thumb_media_id:%s" % (media_id, thumb_media_id)
    elif isinstance(message, LocationMessage):
        location = message.location
        scale = message.scale
        label = message.label
        resp = "location: %s, scale: %s, lable: %s" %(location, scale, label)
    elif isinstance(message, LinkMessage):
        title = message.title
        description = message.description
        url = message.url
        resp = "title: %s, desc: %s, url: %s" %(title, description, url)
    reply = (u'type: %s, target: %s, source: %s, time: %s, content:%s, response: %s'%(type, target, source, time, content, resp))
    #wechat.send_text_message(target,  "hello world")
    return reply



