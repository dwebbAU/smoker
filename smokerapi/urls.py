from django.conf.urls import url,include
from smokerapi import views

urlpatterns = [
    url(r'^sensordata/$',views.SensorDataList.as_view()),
    url(r'^sensordata/(?P<pk>[0-9]+)/$',views.SensorDataDetail.as_view()),
    url(r'^devices/$',views.UserList.as_view()),
    url(r'^devices/(?P<pk>[0-9]+)/$',views.UserDetail.as_view()),
    url(r'^instructions/(?P<pk>[0-9]+)/$',views.InstructionDetail.as_view()),
]
