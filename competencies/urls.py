from django.conf.urls import patterns, url

from competencies import views

urlpatterns = patterns('',
    # My urls
    url(r'^$', views.index, name='index'),
    url(r'^schools/$', views.schools, name='schools'),
    url(r'^schools/(?P<school_id>\d+)/$', views.school, name='school'),
    url(r'^schools/(?P<school_id>\d+)/subject_area/(?P<subject_area_id>\d+)/$', 
        views.subject_area, name='subject_area'),
    url(r'^schools/(?P<school_id>\d+)/subject_area/(?P<subject_area_id>\d+)/competency_area/(?P<competency_area_id>\d+)/$', 
        views.competency_area, name="competency_area"),
    url(r'^entire_system/$', views.entire_system, name='entire_system'),
)
