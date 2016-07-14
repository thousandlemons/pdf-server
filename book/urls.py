from django.conf.urls import url

from book import views

urlpatterns = [
    url(r'^list/$', views.BookList.as_view()),
    url(r'^detail/(?P<pk>[1-9]\d*)/$', views.BookDetail.as_view()),
    url(r'^toc/(?P<pk>[1-9]\d*)/$', views.BookToc.as_view())
]
