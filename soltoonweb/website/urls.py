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
                  url(r'^user/edit/email$', views.EnterEmail.as_view(),
                      name='soltoonwebsite_edit_email'),
                  url(r'^user/edit-soltoon/$', views.EditSoltoon.as_view(),
                      name='soltoonwebsite_edit_soltoon'),
                  url(r'^user/signup/$', views.Signup.as_view(),
                      name='soltoonwebsite_signup'),
                  url(r'^user/reset/$', views.PasswordReset.as_view(),
                      name='soltoonwebsite_reset_password'),
                  url(r'^user/reset/done$', views.PasswordResetDone.as_view(),
                      name='password_reset_done'),
                  url(
                      r'^user/reset/confirm/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
                      views.PasswordResetConfirm.as_view(),
                      name='password_reset_confirm'),
                  url(r'^user/activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
                      views.ActivateUser.as_view(),
                      name='activate-user'),
                  url(r'^game/competition$', views.Game.as_view(),
                      name='soltoonwebsite_game'),
                  url(r'^game/code/send$', views.CompetitionSendCode.as_view(),
                      name='soltoonwebsite_game_send_code'),
                  url(r'^game/training$', views.TrainingScenarios.as_view(),
                      name='soltoonwebsite_game_training'),
                  url(r'^game/training/(?P<scenario>\d+)/table$', views.TrainingScenariosSubmittions.as_view(),
                      name='soltoonwebsite_game_training_table'),
                  url(r'^game/training/(?P<scenario>\d+)/send$', views.TrainingScenariosSendCode.as_view(),
                      name='soltoonwebsite_game_training_send'),
              ] + static('media/avatars/', document_root='media/avatars')
