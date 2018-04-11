from django.conf.urls import url

from . import views

app_name = 'Agent'

urlpatterns = [
    url(r'^$', views.AgentView.as_view(), name='Agent'),
    url(r'^video/$', views.video, name='video'),
]
