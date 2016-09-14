from django.conf.urls import url

from book import views

urlpatterns = [
    url(r'^list/$', views.BookViewSet.as_view({'get': 'list'})),
    url(r'^detail/(?P<pk>[1-9]\d*)/$', views.BookViewSet.as_view({'get': 'retrieve'})),
    url(r'^toc/(?P<pk>[1-9]\d*)/$', views.BookViewSet.as_view({'get': 'toc'})),
    url(r'^read/(?P<pk>[1-9]\d*)/$', views.BookViewSet.as_view({'get': 'read'})),
    url(r'^read/(?P<pk>[1-9]\d*)/(?P<from_>[1-9]\d*)/$', views.BookViewSet.as_view({'get': 'read'})),
    url(r'^read/(?P<pk>[1-9]\d*)/(?P<from_>[1-9]\d*)/(?P<to>[1-9]\d*)/$',
        views.BookViewSet.as_view({'get': 'read'}))
]
