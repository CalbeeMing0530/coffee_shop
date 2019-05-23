from django.conf.urls import include, url
from users import views

urlpatterns = [
    url(r'^user_register/$', views.user_register),
    #yunpian
    url(r'^for_sms_code/$', views.for_sms_code),
    url(r'^is_code_right/$', views.is_code_right),
]


