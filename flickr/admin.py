from django.contrib import admin
from flickr.models import Photo, FlickrUser, PhotoSet



class PhotoAdmin(admin.ModelAdmin):
    date_hierarchy = 'date_taken'
    list_display = ('title', 'flickr_id', 'user', 'date_taken', 'date_posted', 'last_sync')
    list_display_links = ('title', 'flickr_id')
    list_filter = ('date_taken', 'date_posted')
    #prepopulated_fields = {'slug': ('title',)}
    search_fields = ['title', 'description']
    raw_id_fields = ['user',]

admin.site.register(Photo, PhotoAdmin)


class PhotoSetAdmin(admin.ModelAdmin):
    date_hierarchy = 'date_posted'
    list_display = ('title', 'flickr_id', 'user', 'date_posted', 'last_sync')
    list_display_links = ('title', 'flickr_id')
    list_filter = ('date_posted',)
    #prepopulated_fields = {'slug': ('title',)}
    search_fields = ['title', 'description']
    raw_id_fields = ['photos',]

admin.site.register(PhotoSet, PhotoSetAdmin)


class FlickrUserAdmin(admin.ModelAdmin):
    list_display = ('user', 'username', 'nsid')
    
admin.site.register(FlickrUser, FlickrUserAdmin)