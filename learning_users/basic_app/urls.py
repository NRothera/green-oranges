from django.conf.urls import url
from basic_app import views

app_name = 'basic_app'#since we are using template URLs need to set up app_name

urlpatterns = [
    url(r'^registration/$', views.registration, name = 'registration'),
    url(r'^user_login/$', views.user_login, name = 'user_login')
]
