#!/usr/bin/env python
# encoding: utf-8
from bunch import \
    bunchify #for json.dot.notation instead of json['annoying']['dict']
from datetime import datetime
from django.conf import settings
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.db import models
from taggit.managers import TaggableManager


def ts_to_dt(timestamp):
    return datetime.fromtimestamp(int(timestamp)).strftime('%Y-%m-%d %H:%M:%S')

def unslash(url):
    return url.replace('\\/','/')


class FlickrUserManager(models.Manager):
    
    def update_from_json(self, pk, info, **kwargs):
        person = bunchify(info['person'])
        user_data = {'username': person.username._content, 'realname': person.realname._content,
                     'flickr_id': person.id, 'nsid': person.nsid, 
                     'iconserver': person.iconserver, 'iconfarm': person.iconfarm, 'path_alias': person.path_alias,
                     'photosurl': unslash(person.photosurl._content),
                     'profileurl': unslash(person.profileurl._content),
                     'mobileurl': unslash(person.mobileurl._content), 
                     'last_sync': datetime.now(),                    
                     }
        return self.filter(pk=pk).update(**dict(user_data.items() + kwargs.items()))        
        
        
class FlickrUser(models.Model):
    user = models.OneToOneField(User)
    flickr_id = models.CharField(max_length=50, null=True, blank=True)
    nsid = models.CharField(max_length=32, null=True, blank=True)
    username = models.CharField(max_length=64, null=True, blank=True)
    realname = models.CharField(max_length=64, null=True, blank=True)
    photosurl = models.URLField(verify_exists=False, max_length=255, null=True, blank=True)
    profileurl = models.URLField(verify_exists=False, max_length=255, null=True, blank=True)
    mobileurl = models.URLField(verify_exists=False, max_length=255, null=True, blank=True)    
    iconserver = models.CharField(max_length=4, null=True, blank=True)
    iconfarm = models.PositiveSmallIntegerField(null=True, blank=True)
    path_alias = models.CharField(max_length=32, null=True, blank=True)
    
    token = models.CharField(max_length=128, null=True, blank=True)
    perms = models.CharField(max_length=32, null=True, blank=True)
    last_sync = models.DateTimeField(auto_now=True, auto_now_add=True)
    
    objects = FlickrUserManager()
    
    class Meta:
        ordering = ['id']
        
    def __unicode__(self):
        return u"%s" % self.username
    

class FlickrModel(models.Model):
    flickr_id = models.CharField(unique=True, db_index=True, max_length=50)
    user = models.ForeignKey(FlickrUser)    
    show = models.BooleanField(default=True) #show the photo on your page?
    last_sync = models.DateTimeField(auto_now=True, auto_now_add=True)
    
    class Meta:
        abstract = True
    
    
FLICKR_LICENSES = (
    ('0', 'All Rights Reserved'),
    ('1', 'Attribution-NonCommercial-ShareAlike License'),
    ('2', 'Attribution-NonCommercial License'),
    ('3', 'Attribution-NonCommercial-NoDerivs License'),
    ('4', 'Attribution License'),
    ('5', 'Attribution-ShareAlike License'),
    ('6', 'Attribution-NoDerivs License'),
)


class BigIntegerField(models.IntegerField):
    """
    Defines a PostgreSQL compatible IntegerField needed to prevent 'integer 
    out of range' with large numbers.
    """
    def get_internal_type(self):
        return 'BigIntegerField'

    def db_type(self):
        if settings.DATABASE_ENGINE == 'oracle':
            db_type = 'NUMBER(19)'
        else:
            db_type = 'bigint'
        return db_type

        
class PhotoManager(models.Manager):
    
    def visible(self, *args, **kwargs):
        return self.get_query_set().filter(show=True).filter(*args, **kwargs)
    
    def public(self, *args, **kwargs):
        return self.visible(ispublic=1, *args, **kwargs)
    
    def _prepare_data(self, info, sizes, flickr_user=None, exif=None, geo=None):
        photo = bunchify(info['photo'])
        size_json = bunchify(sizes['sizes']['size'])
        photo_data = {
                  'flickr_id': photo.id, 'server': photo.server, 
                  'secret': photo.secret, 'originalsecret': photo.originalsecret, 'farm': photo.farm,
                  'title': photo.title._content, 'description': photo.description._content, 'date_taken': photo.dates.taken,
                  'date_posted': ts_to_dt(photo.dates.posted), 'date_updated': ts_to_dt(photo.dates.lastupdate),
                  'date_taken_granularity':  photo.dates.takengranularity,
                  'ispublic': photo.visibility.ispublic, 'isfriend': photo.visibility.isfriend, 
                  'isfamily': photo.visibility.isfamily,   
                  'license': photo.license, 'tags': photo.tags.tag,        
                  }
        if flickr_user:
            photo_data['user'] = flickr_user
        size_label_conv = {'Square': 'square', 'Thumbnail': 'thumb', 'Small': 'small', 'Medium 640': 'medium', 'Large': 'large', 'Original': 'ori',}
        for size in size_json:
            if size.label in size_label_conv.keys():
                label = size_label_conv[size.label]
                photo_data = dict(photo_data.items() + {
                                label+'_width': size.width, label+'_height': size.height, 
                                label+'_source': size.source, label+'_url': unslash(size.url),
                                }.items())
        for url in photo.urls.url:
            if url.type == 'photopage':
                photo_data['url_page'] = unslash(url._content)
        if exif:
            photo_data['exif'] = str(exif)
            try:
                photo_data['exif_camera'] = exif['photo']['camera']
                for e in bunchify(exif['photo']['exif']):
                    if e.label == 'Exposure':     photo_data['exif_exposure'] = unslash(e.raw._content)
                    if e.label == 'Aperture':     photo_data['exif_aperture'] = unslash(e.clean._content)
                    if e.label == 'ISO Speed':    photo_data['exif_iso'] = e.raw._content
                    if e.label == 'Focal Length': photo_data['exif_focal'] = e.clean._content
                    if e.label == 'Flash':        photo_data['exif_flash'] = e.raw._content
            except KeyError:
                pass
        if geo:
            pass    
        return photo_data
        
    def _add_tags(self, obj, tags, override=False):
        try:
            obj.tags.set(*[tag._content for tag in tags])            
        except KeyError:
            pass
        
    def create_from_json(self, flickr_user, info, sizes, exif=None, geo=None, **kwargs):
        """Create a record for flickr_user"""
        photo_data = self._prepare_data(flickr_user=flickr_user, info=info, sizes=sizes, exif=exif, geo=geo, **kwargs)
        tags = photo_data.pop('tags')
        obj = self.create(**dict(photo_data.items() + kwargs.items()))
        self._add_tags(obj, tags)
        return obj
    
    def update_from_json(self, flickr_id, info, sizes, exif=None, geo=None, update_tags=False, **kwargs):
        """Update a record with flickr_id"""
        photo_data = self._prepare_data(info=info, sizes=sizes, exif=exif, geo=geo, **kwargs)
        tags = photo_data.pop('tags')
        result = self.filter(flickr_id=flickr_id).update(**dict(photo_data.items() + kwargs.items()))
        if result == 1 and update_tags:
            obj = self.get(flickr_id=flickr_id)
            self._add_tags(obj, tags)
        return result
    
    def create_or_update_from_json(self, flickr_user, info, sizes, exif=None, geo=None, **kwargs):
        """Pretty self explanatory"""
        
        

class Photo(FlickrModel):
    
    """http://www.flickr.com/services/api/explore/flickr.photos.getInfo"""    
    
    server = models.PositiveSmallIntegerField()
    farm = models.PositiveSmallIntegerField()       
    secret = models.CharField(max_length=10)
    originalsecret = models.CharField(max_length=10)
    
    title = models.CharField(max_length=255, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    
    date_posted = models.DateTimeField(null=True, blank=True)
    date_taken = models.DateTimeField(null=True, blank=True)
    date_taken_granularity = models.PositiveSmallIntegerField(null=True, blank=True)
    date_updated = models.DateTimeField(null=True, blank=True)
    
    url_page = models.URLField(verify_exists=False, max_length=255, null=True, blank=True)
    tags = TaggableManager(blank=True)
    
    slug = models.SlugField(max_length=255, null=True, blank=True)
    
    """http://www.flickr.com/services/api/explore/flickr.photos.getSizes"""
    
    square_width = models.PositiveIntegerField(null=True, blank=True)
    square_height = models.PositiveIntegerField(null=True, blank=True)
    square_source = models.URLField(verify_exists=False, max_length=255, null=True, blank=True)
    square_url = models.URLField(verify_exists=False, max_length=255, null=True, blank=True)    
    
    thumb_width = models.PositiveIntegerField(null=True, blank=True)
    thumb_height = models.PositiveIntegerField(null=True, blank=True)
    thumb_source = models.URLField(verify_exists=False, max_length=255, null=True, blank=True)
    thumb_url = models.URLField(verify_exists=False, max_length=255, null=True, blank=True)
    
    small_width = models.PositiveIntegerField(null=True, blank=True)
    small_height = models.PositiveIntegerField(null=True, blank=True)
    small_source = models.URLField(verify_exists=False, max_length=255, null=True, blank=True)
    small_url = models.URLField(verify_exists=False, max_length=255, null=True, blank=True)
    
    medium_width = models.PositiveIntegerField(null=True, blank=True)
    medium_height = models.PositiveIntegerField(null=True, blank=True)
    medium_source = models.URLField(verify_exists=False, max_length=255, null=True, blank=True)
    medium_url = models.URLField(verify_exists=False, max_length=255, null=True, blank=True)
    
    large_width = models.PositiveIntegerField(null=True, blank=True)
    large_height = models.PositiveIntegerField(null=True, blank=True)
    large_source = models.URLField(verify_exists=False, max_length=255, null=True, blank=True)
    large_url = models.URLField(verify_exists=False, max_length=255, null=True, blank=True)
    
    ori_width = models.PositiveIntegerField(null=True, blank=True)
    ori_height = models.PositiveIntegerField(null=True, blank=True)
    ori_source = models.URLField(verify_exists=False, max_length=255, null=True, blank=True)
    ori_url = models.URLField(verify_exists=False, max_length=255, null=True, blank=True)
    
    """http://www.flickr.com/services/api/explore/flickr.photos.getExif
    Lots of data varying type and values, let's just put'em (json string in exif) there and we'll think later."""
    
    exif = models.TextField(null=True, blank=True)
    exif_camera = models.CharField(max_length=50, null=True, blank=True)
    exif_exposure = models.CharField(max_length=10, null=True, blank=True)
    exif_aperture = models.CharField(max_length=10, null=True, blank=True)
    exif_iso = models.IntegerField(null=True, blank=True)
    exif_focal = models.CharField(max_length=10, null=True, blank=True)
    exif_flash = models.CharField(max_length=20, null=True, blank=True)
    
    """http://www.flickr.com/services/api/explore/flickr.photos.getPerms"""
    
    ispublic = models.NullBooleanField()
    isfriend = models.NullBooleanField()
    isfamily = models.NullBooleanField()
    
    """http://www.flickr.com/services/api/explore/flickr.photos.geo.getLocation"""
    
    geo_latitude = models.FloatField(null=True, blank=True)
    geo_longitude = models.FloatField(null=True, blank=True)
    geo_accuracy = models.PositiveSmallIntegerField(null=True, blank=True)
    
    license = models.CharField(max_length=50, choices=FLICKR_LICENSES, default=0)

    objects = PhotoManager()
        
    class Meta:
        ordering = ('-date_posted', '-date_taken',)
        get_latest_by = 'date_posted'

    def __unicode__(self):
        return u'%s' % self.title

    def get_absolute_url(self):
        return reverse('flickr_photo', args=[self.flickr_id,])
    



class PhotoSetManager(models.Manager):

    def visible(self, *args, **kwargs):
        return self.get_query_set().filter(show=True).filter(*args, **kwargs)
    
    def _add_photos(self, obj, photos):
        for photo in photos:
            try:
                flickr_photo = Photo.objects.get(flickr_id=photo.id)
                obj.photos.add(flickr_photo)
            except Exception as e:
                pass   
    
    def _prepare_data(self, info, photos, flickr_user=None, exif=None, geo=None):
        photoset = bunchify(info)
        photos = bunchify(photos['photoset']['photo'])

        data = {  'flickr_id': photoset.id, 'server': photoset.server, 
                  'secret': photoset.secret, 'farm': photoset.farm, 'primary': photoset.primary,
                  'title': photoset.title._content, 'description': photoset.description._content,
                  'date_posted': ts_to_dt(photoset.date_create), 'date_updated': ts_to_dt(photoset.date_update),
                  'photos': photos,                          
                  }
        if flickr_user:
            data['user'] = flickr_user
        return data
    
    
    def create_from_json(self, flickr_user, info, photos, **kwargs):
        """Create a record for flickr_user"""
        photoset_data = self._prepare_data(flickr_user=flickr_user, info=info, photos=photos, **kwargs)
        photos = photoset_data.pop('photos')
        obj = self.create(**dict(photoset_data.items() + kwargs.items()))
        self._add_photos(obj, photos)
        return obj
    
    
    
class PhotoSet(FlickrModel):
    """http://www.flickr.com/services/api/explore/flickr.photosets.getInfo"""
        
    server = models.PositiveSmallIntegerField()    
    farm = models.PositiveSmallIntegerField()
    secret = models.CharField(max_length=10)
    
    title = models.CharField(max_length=200)
    description = models.TextField(null=True, blank=True)
    primary = models.CharField(max_length=50, null=True, blank=True) #flickr id of primary photo
    
    date_posted = models.DateTimeField(null=True, blank=True)
    date_updated = models.DateTimeField(null=True, blank=True)
    
    photos = models.ManyToManyField(Photo, null=True, blank=True)
    
    objects = PhotoSetManager()
        
    class Meta:
        ordering = ('-date_posted', '-id',)
        get_latest_by = 'date_posted'

    def __unicode__(self):
        return u'%s' % self.title

    def get_absolute_url(self):
        return reverse('flickr_photoset', args=[self.flickr_id,])
    
    def cover(self):
        try:
            return Photo.objects.get(flickr_id=self.primary)
        except Photo.DoesNotExist:
            try:
                return Photo.objects.filter(photoset__id__in=[self.id,]).latest()
            except Photo.DoesNotExist:
                pass
    
    
class JsonCache(models.Model):
    
    flickr_id = models.CharField(max_length=50, null=True, blank=True)
    info = models.TextField(null=True, blank=True)
    sizes = models.TextField(null=True, blank=True)
    exif = models.TextField(null=True, blank=True)
    geo = models.TextField(null=True, blank=True)
    exception = models.TextField(null=True, blank=True)
    added = models.DateTimeField(auto_now=True, auto_now_add=True)


