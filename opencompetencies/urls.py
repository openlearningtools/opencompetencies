from django.conf.urls import patterns, include, url
from django.conf import settings
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

import os

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # My urls
    url(r'^', include('competencies.urls', namespace='competencies')),
                       
    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),

    # Auth urls
    url(r'^login/', 'django.contrib.auth.views.login', name='login'),
    url(r'^logout/', 'competencies.views.logout_view', name='logout_view'),
    url(r'^profile/', 'competencies.views.profile', name='profile'),
    url(r'^password_change/', 'competencies.views.password_change_form', name='password_change_form'),
    url(r'^password_change_successful/', 'competencies.views.password_change_successful', name='password_change_successful'),
)


# Set up static files appropriate to environment
if os.environ.get('DEPLOY_ENVIRONMENT', None) == 'aws':
    urlpatterns += staticfiles_urlpatterns()
else:

    # heroku static files:
    urlpatterns += patterns('',
                            (r'^static/(.*)$', 'django.views.static.serve',
                             {'document_root': settings.STATIC_ROOT}),
                            )
