from django.conf.urls import url, include
from api import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^predict/$', views.predict, name='predict')
]
