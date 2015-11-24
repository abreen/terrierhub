from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^api/(?P<function>.+)$', views.api, name='api'),
    url(r'^(?P<school>[^/]+)/$', views.school, name='school'),
    #url(r'^(?P<school>.+)/(?P<dept>.+)/$', views.department, name='department'),
    url(r'^(?P<school>.+)/(?P<dept>.+)/(?P<num>[0-9]+)$', views.course, name='course'),
  #  url(r'^(?P<school>.+)/(?P<dept>.+)/(?P<num>[0-9]+)/(?P<section>.+)$', views.section, name='section'),
]


