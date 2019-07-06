from django.conf.urls import include, url
from coffee import views

urlpatterns = [
    #url(r'^$', views.index),
    #buy drinkings
    url(r'^coffee_item/$', views.coffee_item),
    url(r'^tea_item/$', views.tea_item),
    url(r'^package/$', views.package),
    url(r'^search_coffeebar_nearby/$', views.search_coffeebar_nearby),
    #drinking operations
    url(r'^store_cart_data/$', views.store_cart_data),
    url(r'^delete_cart_session/$', views.delete_cart_session),
    url(r'^delete_drinking/$', views.delete_drinking),
    url(r'^temp_0/$', views.temp_0),
    url(r'^modify_cart_data/$', views.modify_cart_data),
    url(r'^get_cart_session/$', views.get_cart_session),
    url(r'^balance_cart_stuff/$', views.balance_cart_stuff),
    url(r'^generate_extraction_code/(?P<coffee_id>([^/]+))/(?P<coffee_count>([^/]+))/(?P<type>([^/]+))/$', views.generate_extraction_code),
    url(r'^get_code/(?P<coffee_id>([^/]+))/(?P<coffee_count>([^/]+))/(?P<type>([^/]+))/$', views.get_code),
    #wei_xin_api
    url(r'^weixin_pay/$', views.weixin_pay),
    url(r'^weixin_pay_success/(?P<last_price>([^/]+))/(?P<coupon_id>([^/]+))/$', views.weixin_pay_success),
    url(r'^weixin_pay_failure/$', views.weixin_pay_failure),
    #personal center
    url(r'^my_coffee_coupon/$', views.my_coffee_coupon),
    url(r'^coupon/$', views.coupon),
    url(r'^historical_order/$', views.historical_order),
    url(r'^invited_gift/$', views.invited_gift),
    url(r'^user_center/$', views.user_center),
    url(r'^edit_drinking/(?P<drinking_id>.+)$', views.edit_drinking),
    url(r'^edit_drinking_info/$', views.edit_drinking_info),
    url(r'^drinking_setting/$', views.drinking_setting),
    url(r'^order_detail/(?P<order_id>.+)$', views.order_detail),
    url(r'^about_us/$', views.about_us),
    url(r'^dispatch_coupon/$', views.dispatch_coupon),
    url(r'^coupon_setting/$', views.coupon_setting),
    url(r'^add_coupon/$', views.add_coupon),
    url(r'^add_coupon_operation/$', views.add_coupon_operation),
    url(r'^edit_coupon/(?P<id>.+)$', views.edit_coupon),
    url(r'^edit_coupon_operation/$', views.edit_coupon_operation),
    url(r'^delete_coupon_operation/$', views.delete_coupon_operation),

]

