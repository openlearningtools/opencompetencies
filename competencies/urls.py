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

    # entire_system/id: List the entire system for a given school.
    url(r'^entire_system/(?P<school_id>\d+)/$', views.entire_system, name='entire_system'),


    # --- Authorization pages ---
    # no_edit_permission: Message that user does not have permission required to edit current elements.
    url(r'^no_edit_permission/(?P<school_id>\d+)/$', views.no_edit_permission, name='no_edit_permission'),


    # --- Edit System pages ---
    # edit_school: Allows editing of a school's subject areas.
    url(r'^edit_school/(?P<school_id>\d+)/$', views.edit_school, name='edit_school'),

    # edit_subject_area: Allows editing of a subject area's subdiscipline areas.
    url(r'^edit_subject_area/(?P<subject_area_id>\d+)/$', views.edit_subject_area, name='edit_subject_area'),

    # edit_sa_competency_areas: Allows editing of competencies for a general subject area.
    url(r'^edit_sa_competency_areas/(?P<subject_area_id>\d+)/$', views.edit_sa_competency_areas, name='edit_sa_competency_areas'),

    # edit_sda_competency_areas: Allows editing of competencies for a subdiscipline area.
    url(r'^edit_sda_competency_areas/(?P<subdiscipline_area_id>\d+)/$', views.edit_sda_competency_areas, name='edit_sda_competency_areas'),

    # edit_competency_area: Allows editing of a competency area's essential understandings.
    url(r'^edit_competency_area/(?P<competency_area_id>\d+)/$', views.edit_competency_area, name='edit_competency_area'),

    # edit_levels: Allows editing of levels for a given competency area.
    url(r'^edit_levels/(?P<competency_area_id>\d+)/$', views.edit_levels, name='edit_levels'),

    # edit_essential_understanding: Allows editing of the learning targets
    #  associated with an essential understanding.
    url(r'^edit_essential_understanding/(?P<essential_understanding_id>\d+)/$', views.edit_essential_understanding, name='edit_essential_understanding'),

    # edit_order: Allows editing the order of any child elements.
    url(r'^edit_order/(?P<school_id>\d+)/$', views.edit_order, name='edit_order'),

    # change_order: No template; changes the order of an element, and redirects to edit_order.
    url(r'^change_order/(?P<school_id>\d+)/(?P<parent_type>\w+)/(?P<parent_id>\d+)/(?P<child_type>\w+)/(?P<child_id>\d+)/(?P<direction>\w+)/$', views.change_order, name='change_order'),

    # edit_visibility: Allows toggling of public/ private mode for all elements.
    url(r'^edit_visibility/(?P<school_id>\d+)/$', views.edit_visibility, name='edit_visibility'),

    # change_visibility: No template; changes the visibility of an elment, and redirects to edit_visibility.
    url(r'^change_visibility/(?P<school_id>\d+)/(?P<object_type>\w+)/(?P<object_pk>\d+)/(?P<visibility_mode>\w+)/$', views.change_visibility, name='change_visibility'),


    # --- Pathways pages ---
    # pathways: Shows all the pathways for a given school.
    url(r'^pathways/(?P<school_id>\d+)/$', views.pathways, name='pathways'),

    # pathway/id: Shows the entire system for a given school, with that pathway highlighted.
    #  Later, will be a flag that stays active, highlighting elements of the pathway on every view page.
    url(r'^pathway/(?P<pathway_id>\d+)/$', views.pathway, name='pathway'),

    # create_pathway: Allows user to create a pathway. Links to pages that edit the pathway.
    url(r'^create_pathway/(?P<school_id>\d+)/$', views.create_pathway, name='create_pathway'),

    # edit_pathway: Allows user to add or remove elements in a pathway.
    url(r'^edit_pathway/(?P<pathway_id>\d+)/$', views.edit_pathway, name='edit_pathway'),

    # edit_pw_visibility: Allows toggling of public/ private mode for each pathway.
    url(r'^edit_pw_visibility/(?P<school_id>\d+)/$', views.edit_pw_visibility, name='edit_pw_visibility'),

    # change_pw_visibility: No template; changes the visibility of a pathway, and redirects to edit_pw_visibility.
    url(r'^change_pw_visibility/(?P<school_id>\d+)/(?P<pathway_pk>\d+)/(?P<visibility_mode>\w+)/$', views.change_pw_visibility, name='change_pw_visibility'),


    # --- Forking pages ---
    # fork: Page offering an empty school the opportunity to fork an established school.
    url(r'^schools/(?P<school_id>\d+)/fork/$', views.fork, name='fork'),

    # confirm_fork: Confirms that a fork was successful.
    url(r'^schools/(?P<forking_school_id>\d+)/fork/(?P<forked_school_id>\d+)/$',
        views.confirm_fork, name='confirm_fork'),

    # new_school: Create a new school.
    url(r'^new_school/$', views.new_school, name='new_school'),

)
