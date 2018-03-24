from django.conf.urls import url
from django.contrib.auth import views as auth_views

app_name = 'Login'

urlpatterns = [
    url(r'^$', auth_views.login, name='Login',
        kwargs={'redirect_authenticated_user': True}),
    url(r'^logout/', auth_views.logout, {'next_page': '/account/login'}, name='Logout'),
]
