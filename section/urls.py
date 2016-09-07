from django.conf.urls import url

from section import views

urlpatterns = [
    url(r'^children/(?P<pk>[1-9]\d*)/$', views.SectionViewSet.as_view({'get': 'children'})),
    url(r'^detail/(?P<pk>[1-9]\d*)/$', views.SectionViewSet.as_view({'get': 'retrieve'})),
    url(r'^versions/(?P<pk>[1-9]\d*)/$', views.SectionViewSet.as_view({'get': 'versions'})),
    url(r'^toc/(?P<pk>[1-9]\d*)/$', views.SectionViewSet.as_view({'get': 'partial_toc'}))
]
