from django.conf.urls import url
from . import views
from django.contrib.auth.views import logout, login

urlpatterns = [
    #Wireless
    url(r'^wireless/$', views.dev_info, name="dev_info"),
    url(r'^wireless/log$', views.log, name="log"),
    url(r'^wireless/toggle/(?P<devId>[0-9.]+)/$', views.on_off),
    url(r'^wireless/givemelogs$', views.givemelogs),
    url(r'^wireless/getDevInfo$', views.getDevInfo),
    url(r'^wireless/update/', views.update),
    url(r'^wireless/setting/$', views.log_setting),
    url(r'^wireless/signal/\d$', views.signal),
    url(r'^wireless/check/$', views.check),
    #DB
    url(r'^$', views.index, name="index"),
    url(r'^group/$', views.group, name="group"),
    url(r'^group/create/$', views.group_create, name="group_create"),
    url(r'^group/create/db/$', views.group_create_db, name="group_create_db"),
    url(r'^group/in/(?P<groupID>[0-9]+)/$', views.group_in, name="group_in"),
    url(r'^actor_info/(?P<actorID>[0-9]+)/$', views.actor_info),
    url(r'^login/', login, name="login"),
    url(r'^logout/', logout, {'next_page': 'index', }, name="logout"),
    url(r'^signup/', views.signup, name="signup"),
	url(r'^movie_info/(?P<movieID>[0-9]+)/$', views.movie_info),
	url(r'^search/',views.search),
	url(r'^director_info/(?P<directorID>[0-9.]+)/$', views.director_info),
]
