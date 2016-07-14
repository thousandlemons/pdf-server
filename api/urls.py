from django.conf.urls import url, include

urlpatterns = [
    url(r'^book/', include('book.urls')),
    url(r'^section/', include('section.urls'))
]
