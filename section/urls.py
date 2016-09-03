from django.conf.urls import url

from section import views

urlpatterns = [
    url(r'^children/(?P<pk>[1-9]\d*)/$', views.ChildrenList.as_view()),
    url(r'^detail/(?P<pk>[1-9]\d*)/$', views.SectionDetail.as_view()),
    url(r'^wordcloud/(?P<pk>[1-9]\d*)/$', views.WordCloud.as_view()),
]
