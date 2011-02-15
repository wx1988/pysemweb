from django.conf.urls.defaults import *


urlpatterns = patterns('webui.views',
    (r'^$','index'),
    (r'^view/$','viewinfo'),
    (r'^schema/$','viewschema'),
)
