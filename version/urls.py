from django.conf.urls import url

from version import views

urlpatterns = [
    url(r'list/$', views.VersionList.as_view()),
    url(r'detail/(?P<pk>[1-9]+)/$', views.VersionDetail.as_view()),
    url(r'create/$', views.VersionCreate.as_view()),
    url(r'update/$', views.VersionUpdate.as_view()),
    url(r'delete/$', views.VersionDelete.as_view()) 
]