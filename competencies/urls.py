from django.conf.urls import patterns, url

from competencies import views

urlpatterns = patterns('',
    # My urls

    # Open Competencies home page
    url(r'^$', views.index, name='index'),

    # schools: List of all schools participating in Open Competencies
    url(r'^schools/$', views.schools, name='schools'),

    # school: Detail view for a school, showing subject areas.
    url(r'^schools/(?P<school_id>\d+)/$', views.school, name='school'),

    # subject_areas/id: List of all subdiscipline areas for a school.
    url(r'^subject_areas/(?P<subject_area_id>\d+)/$', views.subject_area, name='subject_area'),

    # subdiscipline_areas/id: List all the competency areas for a subdiscipline area.
    url(r'^subdiscipline_areas/(?P<subdiscipline_area_id>\d+)/$', views.subdiscipline_area, name='subdiscipline_area'),

    # competency_areas/id: List all essential understandings for a competency area.
    url(r'^competency_areas/(?P<competency_area_id>\d+)/$', views.competency_area, name='competency_area'),




    # fork: Page offering an empty school the opportunity to fork an established school.
    url(r'^schools/(?P<school_id>\d+)/fork/$', views.fork, name='fork'),

    # edit_system: Allows editing of an entire school's competency system.
    url(r'^schools/(?P<school_id>\d+)/edit_system/$', views.edit_system, name='edit_system'),

    # confirm_fork: Confirms that a fork was successful.
    url(r'^schools/(?P<forking_school_id>\d+)/fork/(?P<forked_school_id>\d+)/$',
        views.confirm_fork, name='confirm_fork'),

    # new_school: Create a new school.
    url(r'^new_school/$', views.new_school, name='new_school'),

    # subject_area: Lists the competency areas for a given subject area, and all its subdiscipline areas.
    url(r'^schools/(?P<school_id>\d+)/subject_area/(?P<subject_area_id>\d+)/$', 
        views.subject_area, name='subject_area'),
    # competency_area: Lists the essential understandings and learning targets for a given competency area.
    url(r'^schools/(?P<school_id>\d+)/subject_area/(?P<subject_area_id>\d+)/competency_area/(?P<competency_area_id>\d+)/$', 
        views.competency_area, name="competency_area"),

    # Lists all information for a given school, from subject areas down to learning targets.
    url(r'^entire_system/$', views.entire_system, name='entire_system'),

)
