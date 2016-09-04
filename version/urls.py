from django.conf.urls import url

from version import views

urlpatterns = [
    url(r'list/$', views.VersionViewSet.as_view({'get': 'list'})),
    url(r'detail/(?P<pk>[1-9]+)/$', views.VersionViewSet.as_view({'get': 'retrieve'})),
    url(r'create/$', views.VersionViewSet.as_view({'put': 'create'})),
    url(r'update/(?P<pk>[1-9]+)/$', views.VersionViewSet.as_view({'post': 'update'})),
    url(r'delete/(?P<pk>[1-9]+)/$', views.VersionViewSet.as_view({'delete': 'destroy'}))
]
