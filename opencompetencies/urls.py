from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'opencompetencies.views.home', name='home'),
    # url(r'^opencompetencies/', include('opencompetencies.foo.urls')),

    # My urls
    url(r'^$', 'competencies.views.index'),
    url(r'^schools/$', 'competencies.views.schools'),
    url(r'^schools/(?P<school_id>\d+)/$', 'competencies.views.school'),
    url(r'^entire_system/$', 'competencies.views.entire_system'),
                       
    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
)
