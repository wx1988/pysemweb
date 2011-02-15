from django.conf.urls.defaults import *

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Example:
    # (r'^MusicSemNet/', include('MusicSemNet.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # (r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    (r'^admin/', include(admin.site.urls)),
    (r'^sparql/', include('sparqlengine.urls')),
    (r'^webui/', include('webui.urls')),                       
    #(r'^test/', include('sparqlengine.views.index')),
)
