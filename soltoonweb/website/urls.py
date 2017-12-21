from django.conf.urls import url
from django.contrib.auth import views as auth_views

from website import views

urlpatterns = [
    url(r'^home/', views.Home.as_view(),
        name='soltoonwebsite_home'),
    url(r'^login/', views.Login.as_view(),
        name='soltoonwebsite_login'),
    url(r'^game/', views.Game.as_view(),
        name='soltoonwebsite_game'),
]
