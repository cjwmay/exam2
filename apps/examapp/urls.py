from django.conf.urls import url
from . import views           # So we can call functions from our routes!
urlpatterns = [
	url(r'^main$', views.index),
    url(r'^checkregister$', views.checkregister),
    url(r'^checklogin$', views.checklogin),
	url(r'^logout$', views.logout),
    url(r'^quotes$', views.success),
	url(r'^addquote$', views.addquote),
	url(r'^addfav$', views.addfav),
	url(r'^remove$', views.remove),
	url(r'^users/(?P<id>\d+)$', views.userbyid, name = "userbyid"),
]
