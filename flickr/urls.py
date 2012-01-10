from django.conf.urls.defaults import patterns, url

urlpatterns = patterns('',
    url(r'^auth/$', "flickr.views.auth", name="flickr_auth"),
    url(r'^method/(?P<method>.*)/$', "flickr.views.method_call", name="flickr_method"),
    url(r'^set/(?P<flickr_id>.*)/$', "flickr.views.photoset", name="flickr_photoset"),
    url(r'^photo/(?P<flickr_id>.*)/$', "flickr.views.photo", name="flickr_photo"),
    url(r'^$', "flickr.views.index", name="flickr_index"),
)


