from django.conf.urls import url
from . import views           # So we can call functions from our routes!
urlpatterns = [
	url(r'^$', views.index),
    url(r'^checkregister$', views.checkregister),
    url(r'^checklogin$', views.checklogin),
    url(r'^success$', views.success),
]
