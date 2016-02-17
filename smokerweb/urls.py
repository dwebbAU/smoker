from django.conf.urls import url,include
from smokerweb import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    url(r'^$',views.CookDashboard),
    url(r'^accounts/login/$', auth_views.login),
    url(r'^accounts/logout/$', auth_views.logout),
]
