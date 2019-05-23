from django.conf.urls import include, url
from ui import views

urlpatterns = [
    url(r'^$', views.index),
    url(r'^callback$', views.callback),
]
