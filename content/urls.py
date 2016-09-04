from django.conf.urls import url

from content import views

urlpatterns = [
    # Version key is optional for Immediate Text and Aggregate Text,
    # but required for Post.
    url(r'immediate/(?P<pk_section>[1-9]+)/(?P<pk_version>[1-9]+)?/$', views.ContentImmediate.as_view()),
    url(r'aggregate/(?P<pk_section>[1-9]+)/(?P<pk_version>[1-9]+)?/$', views.ContentAggregate.as_view()),
    url(r'post/(?P<pk_section>[1-9]+)/(?P<pk_version>[1-9]+)/$', views.ContentPost.as_view())
]