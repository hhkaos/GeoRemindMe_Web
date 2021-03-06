from django.conf.urls.defaults import *

urlpatterns = patterns('geoauth.views',
    (r'^request_token/$', 'token_request'),
    (r'^authorize/$', 'authorize_token_request'),
    (r'^access_token/$', 'access_token_request'),
    (r'^client_request_token/(?P<provider>[^/]*)/$', 'client_token_request'),
    (r'^authorized/(?P<provider>[^/]*)/$', 'client_access_request'),
    (r'^authenticate/(?P<provider>[^/]*)/$', 'authenticate_request'),
)