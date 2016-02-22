from django.conf.urls import url,include
from smokerapi import views

urlpatterns = [
    url(r'^sensordata/$',views.SensorDataList.as_view()),
    url(r'^sensordata/(?P<pk>[0-9]+)/$',views.SensorDataDetail.as_view()),
    url(r'^controllers/$',views.ControllerList.as_view()),
    url(r'^controllers/(?P<pk>[0-9]+)/$',views.UserDetail.as_view()),
    url(r'^recipes/$',views.RecipeList.as_view()),
    url(r'^recipes/(?P<pk>[0-9]+)/$',views.RecipeDetail.as_view()),
    url(r'^cooks/$',views.CookList.as_view()),
    url(r'^cooks/(?P<pk>[0-9]+)/$',views.CookDetail.as_view()),
]
