# -*- coding: utf-8 -*-  
from wechat_sdk import WechatConf

#callback = 'http://www.coffeen.cn/ui/callback'
#appid = 'wx90d5fbf708203305'
#appsecret = '776dcc3289fb5e5643c6c7e621868202'
#
#conf = WechatConf(
#    token='puming',
#    appid= 'wx90d5fbf708203305',
#    appsecret = '776dcc3289fb5e5643c6c7e621868202',
#    encoding_aes_key = 'HQFU6gjzs8HHBmr9eJuRZ8Hb8hePPtl7MHWjI9mjOtO'
#)


callback = 'http://www.coffeen.cn/ui/callback'
appid = 'wx956cb8fc49d507e1'
appsecret = 'f02960752f990f30f6769a5fb34ab13d'
#微信商户平台
mch_id = 1528430881
#mch_id = 1508197991
api_key = '1mmax4iufeecorntfjvf75tyw8knc5p7'
#api_key = 'chengyiwei110119820180301211020u'
order_url = 'https://api.mch.weixin.qq.com/pay/unifiedorder'
#关注自动回复
content = '感谢您关注咖啡N次方！\n\n<a href="http://www.coffeen.cn/users/user_register/">这位同学，您迟到了！身边的小伙伴已经领到了50元代金券，赶快点我领取吧</a>'
#自动回复
re_content = '如有购买、领取咖啡或相关事宜咨询或投诉，请拨打客服电话4008931580'

conf = WechatConf(
    #微信公众号
    token='puming',
    appid= 'wx956cb8fc49d507e1',
    appsecret = 'f02960752f990f30f6769a5fb34ab13d',
    encoding_aes_key = '5mZlScaMYb37KLIi12bbBqrWB4neOPzFPVwWLLeIbqO',
)

