from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index, name = 'index'),
    url(r'^newres$', views.newres, name = 'newres'),
    url(r'^create$', views.create, name = 'create'),
    url(r'^details/(?P<id>\d+)$', views.details, name = 'details'),
    url(r'^add/(?P<id>\d+)$', views.add, name = 'add'),
]