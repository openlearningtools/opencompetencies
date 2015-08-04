from django.conf.urls import patterns, url

from competencies import views

urlpatterns = patterns('',
    # My urls

    # --- Open Competencies home page ---

    url(r'^$', views.index, name='index'),


    # --- Simple views of competency system; no opportunity to modify system ---

    # organizations: List of all organizations the user owns, can edit,
    #  and all public organizations.
    url(r'^organizations/$', views.organizations, name='organizations'),

    # organization: Detail view for an organization, showing subject areas.
    url(r'^organizations/(?P<organization_id>\d+)/$', views.organization, name='organization'),

    # sa_summary/id: Show a GSP-style summary for a given subject area.
    url(r'^sa_summary/(?P<sa_id>\d+)/$', views.sa_summary, name='sa_summary'),


    # --- Edit system pages ---

    # edit_sa_summary/id: Edit a summary for a given subject area.
    url(r'^edit_sa_summary/(?P<sa_id>\d+)/$', views.edit_sa_summary, name='edit_sa_summary'),                       

    # organization_admin_summary/id: Summarize an organization.
    url(r'^organization_admin_summary/(?P<organization_id>\d+)/$', views.organization_admin_summary, name='organization_admin_summary'),

    # organization_admin_edit/id: Administer an organization.
    url(r'^organization_admin_edit/(?P<organization_id>\d+)/$', views.organization_admin_edit, name='organization_admin_edit'),

    # fork/id: Fork an existing school into the current school.
    url(r'^fork/(?P<organization_id>\d+)/$', views.fork, name='fork'),

    # --- New element pages ---

    # new_organization: Create a new organization.
    url(r'^new_organization/$', views.new_organization, name='new_organization'),

    # new_sa: Create a new sa, for a specific school.
    url(r'^new_sa/(?P<school_id>\d+)/$', views.new_sa, name='new_sa'),

    # new_sda: Create a new sda, for a specific subject area.
    url(r'^new_sda/(?P<sa_id>\d+)/$', views.new_sda, name='new_sda'),

    # new_ca: Create a new competency area, for a specific general subject area.
    url(r'^new_ca/(?P<sa_id>\d+)/$', views.new_ca, name='new_ca'),

    # new_sda_ca: Create a new competency area, for a specific subdiscipline area.
    url(r'^new_sda_ca/(?P<sda_id>\d+)/$', views.new_sda_ca, name='new_sda_ca'),

    # new_eu: Create a new essential understanding, for a specific ca.
    url(r'^new_eu/(?P<ca_id>\d+)/$', views.new_eu, name='new_eu'),
                       

    # --- Authorization pages ---

    # no_edit_permission: Message that user does not have permission required to edit current elements.
    url(r'^no_edit_permission/(?P<school_id>\d+)/$', views.no_edit_permission, name='no_edit_permission'),


)
