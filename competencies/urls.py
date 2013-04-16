from django.conf.urls import patterns, url

from competencies import views

urlpatterns = patterns('',
    # My urls

    # --- Open Competencies home page ---
    url(r'^$', views.index, name='index'),

    # --- Simple views of competency system; no opportunity to modify system ---
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

    # essential_understandings/id: List all learning targets for an essential understanding.
    url(r'^essential_understandings/(?P<essential_understanding_id>\d+)/$', views.essential_understanding, name='essential_understanding'),


    # --- Edit System pages ---
    # edit_school: Allows editing of a school's subject areas.
    url(r'^edit_school/(?P<school_id>\d+)/$', views.edit_school, name='edit_school'),

    # edit_subject_area: Allows editing of a subject area's subdiscipline areas.
    url(r'^edit_subject_area/(?P<subject_area_id>\d+)/$', views.edit_subject_area, name='edit_subject_area'),


    # --- Forking pages ---
    # fork: Page offering an empty school the opportunity to fork an established school.
    url(r'^schools/(?P<school_id>\d+)/fork/$', views.fork, name='fork'),

    # confirm_fork: Confirms that a fork was successful.
    url(r'^schools/(?P<forking_school_id>\d+)/fork/(?P<forked_school_id>\d+)/$',
        views.confirm_fork, name='confirm_fork'),

    # new_school: Create a new school.
    url(r'^new_school/$', views.new_school, name='new_school'),

)
