from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^(?P<school>[^/]+)/$', views.school, name='school'),
    url(r'^(?P<school>.+)/(?P<dept>.+)/$', views.department, name='department'),
    url(r'^(?P<school>.+)/(?P<dept>.+)/(?P<num>[0-9]+)$', views.course, name='course'),
]
