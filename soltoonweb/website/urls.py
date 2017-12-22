from django.conf.urls import url
from django.contrib.auth import views as auth_views

from website import views

urlpatterns = [
    url(r'^/$', views.Home.as_view(),
        name='soltoonwebsite_home'),
    url(r'^login/', views.Login.as_view(),
        name='soltoonwebsite_login'),
    url(r'^game/$', views.Game.as_view(),
        name='soltoonwebsite_game'),
    url(r'^game/code/upload$', views.upload_code,
        name='soltoonwebsite_uploadcode'),
    url(r'^game/register$', views.RegisterGame.as_view(),
        name='soltoonwebsite_registergame'),
]
