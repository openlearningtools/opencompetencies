from django.conf.urls import patterns, url
from django.contrib.auth.views import login
from users import views

urlpatterns = patterns('',
    # Auth urls
    url(r'^login/', login, {'template_name': 'users/login.html'}, name='login'),
    url(r'^logout/', 'users.views.logout_view', name='logout_view'),
    url(r'^profile/', 'users.views.profile', name='profile'),
    url(r'^password_change/', 'users.views.password_change_form', name='password_change_form'),
    url(r'^password_change_successful/', 'users.views.password_change_successful', name='password_change_successful'),
    url(r'^register/', 'users.views.register', name='register'),                       
)
