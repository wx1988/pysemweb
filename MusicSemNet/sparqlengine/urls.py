from django.conf.urls.defaults import *


urlpatterns = patterns('sparqlengine.views',
    (r'^$','index'),
    (r'^result$','showresult'),
)
