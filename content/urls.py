from django.conf.urls import url

from content import views

urlpatterns = [
    # Version key is optional for Immediate Text and Aggregate Text,
    # but required for Post.
    url(r'immediate/(?P<section_pk>[1-9]\d*)/$', views.ContentViewSet.as_view({'get': 'immediate'})),
    url(r'immediate/(?P<section_pk>[1-9]\d*)/(?P<version_pk>[1-9]+)/$',
        views.ContentViewSet.as_view({'get': 'immediate'})),
    url(r'aggregate/(?P<section_pk>[1-9]\d*)/$', views.ContentViewSet.as_view({'get': 'aggregate'})),
    url(r'aggregate/(?P<section_pk>[1-9]\d*)/(?P<version_pk>[1-9]+)/$',
        views.ContentViewSet.as_view({'get': 'aggregate'})),
    url(r'post/(?P<section_pk>[1-9]\d*)/(?P<version_pk>[1-9]+)/$', views.ContentViewSet.as_view({'post': 'post'}))
]
