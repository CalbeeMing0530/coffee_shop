import CARDCODE.views  as views
from django.conf.urls import url

urlpatterns = [
    url(r'^$', views.CARDCODE.as_view()),
]
            
