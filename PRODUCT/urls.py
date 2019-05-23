import PRODUCT.views  as views
from django.conf.urls import url

urlpatterns = [
    url(r'^$', views.PRODUCT.as_view()),
]
            

