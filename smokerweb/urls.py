from django.conf.urls import url,include
from smokerweb import views

urlpatterns = [
    url(r'^$',views.Index),

]
