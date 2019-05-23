from django.conf.urls import include, url
from django.contrib import admin
from django.http import HttpResponse

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^handlers/', include('handlers.urls')),
    url(r'^', include('ui.urls')),
    url(r'^ui/', include('ui.urls')),
    url(r'^coffee/', include('coffee.urls')),
    url(r'^CARDCODE', include('CARDCODE.urls')),
    url(r'^PRODUCT', include('PRODUCT.urls')),
    url(r'^WEIXIN_PAY', include('WEIXIN_PAY.urls')),
    url(r'^users/', include('users.urls')),
    url(r'^MP_verify_oNsHXm0tO0iNjNtv.txt', lambda x: HttpResponse("oNsHXm0tO0iNjNtv", content_type="text/plain")),
]
