from django.conf.urls import patterns, url

from competencies import views

urlpatterns = patterns('',
    # My urls
    url(r'^$', views.index, name='index'),
    url(r'^schools/$', views.schools, name='schools'),
    url(r'^schools/(?P<school_id>\d+)/$', views.school, name='school'),
    url(r'^entire_system/$', views.entire_system, name='entire_system'),
)
