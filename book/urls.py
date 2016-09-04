from django.conf.urls import url

from book import views

urlpatterns = [
    url(r'^list/$', views.BookViewSet.as_view({'get': 'list'})),
    url(r'^detail/(?P<pk>[1-9]\d*)/$', views.BookViewSet.as_view({'get': 'retrieve'})),
    url(r'^toc/(?P<pk>[1-9]\d*)/$', views.BookViewSet.as_view({'get': 'toc'}))
]
