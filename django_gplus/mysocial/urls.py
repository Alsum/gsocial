from django.conf.urls import url
from django.contrib.auth import views as auth_views
from mysocial import views
urlpatterns = [
    url(r'^$', views.home, name='home'),
    url(r'^accounts/login/$', views.login_view, name='login'),
    url(r'^accounts/logout/$', views.logout_view, name='logout'),
    url(r'^accounts/register/$', views.registration_view, name='auth_register'),
    url(r'^accounts/activate/(?P<activation_key>\w+)/$', views.activation_view, name='activation_view'),
]