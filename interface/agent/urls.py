from django.conf.urls import url
from . import views

app_name = 'Agent'

urlpatterns = [
    url(r'^$', views.AgentView.as_view(), name='Agent'),
    url(r'^video/$', views.video, name='video'),
    url(r'^get_logs/$', views.get_logs, name='get_logs'),
    url(r'^send_command/$', views.send_command, name='send_command')
]
