from django.conf.urls import url,include
from smokerweb import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    url(r'^$',views.Landing),
    url(r'^cooks/(?P<pk>[0-9]+)$',views.CookDashboard,name='cook_dashboard'),
    url(r'^accounts/login/$', auth_views.login),
    url(r'^accounts/logout/$', auth_views.logout),
]
