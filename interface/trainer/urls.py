from django.conf.urls import url
from django.contrib.auth import views as auth_views

from . import views

app_name = 'Trainer'

urlpatterns = [
    url(r'^$', views.TrainerView.as_view(), name='Trainer'),
    url(r'^logout/', auth_views.logout, name='Logout'),
    url(r'^send_command/$', views.send_command, name='send_command'),
    url(r'^video/$', views.video, name='video'),
    url(r'^logger/$', views.loggerFunc, name='logger')

]
