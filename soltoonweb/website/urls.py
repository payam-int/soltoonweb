from django.conf.urls import url
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views

from website import views

urlpatterns = [
    url(r'^$', views.Home.as_view(),
        name='soltoonwebsite_home'),
    url(r'^user/login/$', views.Login.as_view(),
        name='soltoonwebsite_login'),
    url(r'^user/logout/$', views.Logout.as_view(),
        name='soltoonwebsite_logout'),
    url(r'^user/edit/$', views.EditProfile.as_view(),
        name='soltoonwebsite_edit_profile'),
    url(r'^user/signup/$', views.Signup.as_view(),
        name='soltoonwebsite_edit_profile'),
    url(r'^user/signup/shit$', views.EditProfile.as_view(),
        name='activate-user'),
    url(r'^game/$', views.Game.as_view(),
        name='soltoonwebsite_game'),
    url(r'^game/training$', views.TrainingScenarios.as_view(),
        name='soltoonwebsite_game_training'),
    url(r'^game/training/(?P<scenario>\d+)/table$', views.TrainingScenariosSubmittions.as_view(),
        name='soltoonwebsite_game_training_table'),
    url(r'^game/training/(?P<scenario>\d+)/send$', views.TrainingScenariosSendCode.as_view(),
        name='soltoonwebsite_game_training_send'),
    # url(r'^game/code/upload$', views.upload_code,
    #     name='soltoonwebsite_uploadcode'),
    # url(r'^game/register$', views.RegisterGame.as_view(),
    #     name='soltoonwebsite_registergame'),
]+static('media/avatars/',document_root='media/avatars')
