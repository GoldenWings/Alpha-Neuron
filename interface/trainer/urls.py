from django.conf.urls import url
from django.contrib.auth import views as auth_views

from . import views

app_name = 'Trainer'

urlpatterns = [
    url(r'^$', views.TrainerView.as_view(), name='Trainer'),
    url(r'^logout/', auth_views.logout, name='Logout'),
    url(r'^send_command/$', views.send_command, name='send_command'),
    url(r'^start_recording/$', views.start_recording, name='start_recording'),
    url(r'^pause_recording/$', views.pause_recording, name='pause_recording'),
    url(r'^stop_recording/$', views.stop_recording, name='stop_recording'),
    url(r'^video/$', views.video, name='video'),
]
