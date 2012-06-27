from django.contrib import admin
from flickr.models import Photo, FlickrUser, PhotoSet, Collection, PhotoDownload, PhotoSizeData


class PhotoAdmin(admin.ModelAdmin):
    date_hierarchy = 'date_taken'
    list_display = ('thumbnail', 'title', 'flickr_id', 'user', 'date_taken', 'date_posted', 'last_sync')
    list_display_links = ('thumbnail', 'title', 'flickr_id')
    list_filter = ('date_taken', 'date_posted')
    #prepopulated_fields = {'slug': ('title',)}
    search_fields = ['title', 'description']
    raw_id_fields = ['user', ]

admin.site.register(Photo, PhotoAdmin)


class PhotoSetAdmin(admin.ModelAdmin):
    date_hierarchy = 'date_posted'
    list_display = ('thumbnail', 'title', 'flickr_id', 'user', 'date_posted', 'last_sync')
    list_display_links = ('thumbnail', 'title', 'flickr_id')
    list_filter = ('date_posted',)
    #prepopulated_fields = {'slug': ('title',)}
    search_fields = ['title', 'description']
    raw_id_fields = ['photos', ]

admin.site.register(PhotoSet, PhotoSetAdmin)


class CollectionAdmin(admin.ModelAdmin):
    date_hierarchy = 'date_created'
    list_display = ('thumbnail', 'title', 'flickr_id', 'parent', 'user', 'date_created')
    list_display_links = ('thumbnail', 'title', 'flickr_id')
    list_filter = ('date_created',)
    #prepopulated_fields = {'slug': ('title',)}
    search_fields = ['title', 'description']
    raw_id_fields = ['sets', 'parent']

admin.site.register(Collection, CollectionAdmin)


class FlickrUserAdmin(admin.ModelAdmin):
    list_display = ('user', 'username', 'nsid')

admin.site.register(FlickrUser, FlickrUserAdmin)


class DownloadAdmin(admin.ModelAdmin):
    date_hierarchy = 'date_downloaded'
    list_display = ('photo', 'date_downloaded', 'size')
    list_display_links = ('photo', 'date_downloaded')
    list_filter = ('date_downloaded',)
    #prepopulated_fields = {'slug': ('title',)}
    search_fields = ['photo__title', 'photo__flickr_id']

admin.site.register(PhotoDownload, DownloadAdmin)


class PhotoSizeDataAdmin(admin.ModelAdmin):
    list_display = ('photo', 'size', 'source')
    list_filter = ('size',)
    search_fields = ['photo__title', 'photo__flickr_id']

admin.site.register(PhotoSizeData, PhotoSizeDataAdmin)
