import WEIXIN_PAY.views  as views
from django.conf.urls import url

urlpatterns = [
    url(r'^$', views.WEIXIN_PAY.as_view()),
]
            


