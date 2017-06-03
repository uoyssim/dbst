from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^wireless/$', views.dev_info, name="dev_info"),
    url(r'^wireless/log$', views.log, name="log"),
    url(r'^wireless/toggle/(?P<devId>[0-9.]+)/$', views.on_off),
    url(r'^wireless/givemelogs$', views.givemelogs),
    url(r'^wireless/getDevInfo$', views.getDevInfo),
    url(r'^wireless/update/', views.update),
    url(r'^wireless/setting/$', views.log_setting),
    url(r'^wireless/signal/\d$', views.signal),
    url(r'^wireless/check/$', views.check),
    url(r'^$', views.index),
    url(r'^actor_info$', views.actor_info),
]
