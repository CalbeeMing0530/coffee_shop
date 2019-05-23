from django.conf.urls import include, url
from handlers import views

urlpatterns = [
    url(r'^callback$', views.callback),
]
