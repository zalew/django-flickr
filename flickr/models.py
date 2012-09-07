#!/usr/bin/env python
# encoding: utf-8
from bunch import bunchify  # #for json.dot.notation instead of json['annoying']['dict']
from django.conf import settings
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.db import models
from django.utils.timezone import now
from taggit.managers import TaggableManager
from flickr.flickr_spec import FLICKR_PHOTO_SIZES, build_photo_source
from flickr.utils import ts_to_dt, unslash

URL_BASE = getattr(settings, 'FLICKR_URL_BASE', 'http://www.flickr.com/')


class FlickrUserManager(models.Manager):

    def update_from_json(self, pk, info, **kwargs):
        person = bunchify(info['person'])
        user_data = {'username': person.username._content, 'realname': person.realname._content,
                     'flickr_id': person.id, 'nsid': person.nsid, 'ispro': person.ispro,
                     'iconserver': person.iconserver, 'iconfarm': person.iconfarm, 'path_alias': person.path_alias,
                     'photosurl': unslash(person.photosurl._content),
                     'profileurl': unslash(person.profileurl._content),
                     'mobileurl': unslash(person.mobileurl._content),
                     'tzoffset' : person.timezone.offset,
                     #'last_sync': now(),
                     }
        return self.filter(pk=pk).update(**dict(user_data.items() + kwargs.items()))


class FlickrUser(models.Model):
    user = models.OneToOneField(User)
    flickr_id = models.CharField(max_length=50, null=True, blank=True)
    nsid = models.CharField(max_length=32, null=True, blank=True)
    username = models.CharField(max_length=64, null=True, blank=True)
    realname = models.CharField(max_length=64, null=True, blank=True)
    photosurl = models.URLField(max_length=255, null=True, blank=True)
    profileurl = models.URLField(max_length=255, null=True, blank=True)
    mobileurl = models.URLField(max_length=255, null=True, blank=True)
    iconserver = models.CharField(max_length=4, null=True, blank=True)
    iconfarm = models.PositiveSmallIntegerField(null=True, blank=True)
    path_alias = models.CharField(max_length=32, null=True, blank=True)
    ispro = models.NullBooleanField()
    tzoffset = models.CharField(max_length=6, null=True, blank=True)

    token = models.CharField(max_length=128, null=True, blank=True)
    perms = models.CharField(max_length=32, null=True, blank=True)
    last_sync = models.DateTimeField(null=True, blank=True)

    objects = FlickrUserManager()

    class Meta:
        ordering = ['id']

    def __unicode__(self):
        return u"%s" % self.username

    @property
    def flickr_page_url(self):
        if self.username:
            return '%sphotos/%s/' % (URL_BASE, self.username)
        return '%sphotos/%s/' % (URL_BASE, self.nsid)

    def bump(self):
        self.last_sync = now()
        self.save()


class FlickrModel(models.Model):
    flickr_id = models.CharField(unique=True, db_index=True, max_length=50)
    user = models.ForeignKey(FlickrUser)
    show = models.BooleanField(default=True)  # #show the photo on your page?
    last_sync = models.DateTimeField(blank=True, null=True, editable=False)

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
    Defines a PostgreSQL compatible IntegerField needed to prevent 'integer out of range' with large numbers.
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

    allowed_sizes = ['Square', 'Thumbnail', 'Small', 'Medium 640', 'Large', 'Original', ]

    def visible(self, *args, **kwargs):
        return self.get_query_set().filter(show=True).filter(*args, **kwargs)

    def public(self, *args, **kwargs):
        return self.visible(ispublic=1, *args, **kwargs)

    def _prepare_data(self, photo, flickr_user, info=None, exif=None, geo=None, **kwargs):
        """
        Returns a dict with all information related to a photo. As some info
        can be in several parameters, it returns data from the most especific
        one.

        @params photo: data for one photo as returned from 'flickr.people.getPhotos'
        @params info: data for one photo as returned from 'flickr.photos.getInfo'
        @params exif: data for one photo as returned from 'flickr.photos.getExif'
        @params geo: data for one photo as returned from 'flickr.photos.geo.getLocation'
        @params flickr_user: FlickrUser object for the given photo
        @return:    the dict with all photo data.
        """
        photo_bunch = bunchify(photo)
        photo_data = {}
        if info and exif and geo:
            """ Update last_sync only if all the info is retrieved from flickr """
            photo_data.update({'last_sync' : now()})
        if info:
            """ With data returned from 'photos.getInfo' (no need of 'photo' dict)."""
            info_bunch = bunchify(info['photo'])
            photo_info = {
                        'flickr_id': info_bunch.id,
                        'server': info_bunch.server,
                        'farm': info_bunch.farm,
                        'secret': info_bunch.secret,
                        'originalsecret': getattr(info_bunch, 'originalsecret', ''),
                        'originalformat': getattr(info_bunch, 'originalformat', ''),
                        'title': info_bunch.title._content,
                        'description': info_bunch.description._content,
                        'date_posted': ts_to_dt(info_bunch.dates.posted, flickr_user.tzoffset),
                        'date_taken': '%s%s' % (info_bunch.dates.taken, flickr_user.tzoffset),
                        'date_taken_granularity': info_bunch.dates.takengranularity,
                        'date_updated': ts_to_dt(info_bunch.dates.lastupdate, flickr_user.tzoffset),
                        'tags': info_bunch.tags.tag,
                        'ispublic': info_bunch.visibility.ispublic,
                        'isfriend': info_bunch.visibility.isfriend,
                        'isfamily': info_bunch.visibility.isfamily,
                        'license': info_bunch.license,
                        }
            for url in info_bunch.urls.url:
                if url.type == 'photopage':
                    photo_info['url_page'] = unslash(url._content)
        else:
            photo_info = {
                        'flickr_id': photo_bunch.id,
                        'server': photo_bunch.server,
                        'farm': photo_bunch.farm,
                        'secret': photo_bunch.secret,
                        'originalsecret': getattr(photo_bunch, 'originalsecret', ''),
                        'originalformat': getattr(photo_bunch, 'originalformat', ''),
                        'title': photo_bunch.title,
                        'description': getattr(getattr(photo_bunch, 'description', {}), '_content', ''),
                        'date_posted': ts_to_dt(getattr(photo_bunch, 'dateupload', ''), flickr_user.tzoffset),
                        'date_taken': getattr(photo_bunch, 'datetaken', ''),
                        'date_taken_granularity': getattr(photo_bunch, 'datetakengranularity', ''),
                        'date_updated': ts_to_dt(getattr(photo_bunch, 'lastupdate', ''), flickr_user.tzoffset),
                        'tags': getattr(photo_bunch, 'tags', ''),
                        'ispublic': photo_bunch.ispublic,
                        'isfriend': photo_bunch.isfriend,
                        'isfamily': photo_bunch.isfamily,
                        'license': photo_bunch.license,
                        }
            if photo_info['date_taken']:
                photo_info['date_taken'] = '%s%s' % (photo_info['date_taken'], flickr_user.tzoffset)

        photo_data.update(photo_info)

        if flickr_user:
            photo_data.update({'user': flickr_user})

        if exif:
            """ Exif data can only come from 'photos.getExif' """
            photo_data['exif'] = str(exif)
            try:
                photo_data['exif_camera'] = exif['photo']['camera']
                for e in bunchify(exif['photo']['exif']):
                    if e.label == 'Exposure':
                        photo_data['exif_exposure'] = unslash(e.raw._content)
                    if e.label == 'Aperture':
                        photo_data['exif_aperture'] = unslash(e.clean._content)
                    if e.label == 'ISO Speed':
                        photo_data['exif_iso'] = e.raw._content
                    if e.label == 'Focal Length':
                        photo_data['exif_focal'] = e.clean._content
                    if e.label == 'Flash':
                        photo_data['exif_flash'] = e.raw._content
            except KeyError:
                pass
            except AttributeError:  # #'e.clean._content'
                pass

        if geo:
            """ Geo data can come from 'photos.getGeo' """
            try:
                geo_data = {
                    'geo_latitude': geo['photo']['location']['latitude'],
                    'geo_longitude': geo['photo']['location']['longitude'],
                    'geo_accuracy': geo['photo']['location']['accuracy'],
                    }
            except:  # \todo TBD: not really tested
                geo_data = {}
        else:
            geo_data = {
                'geo_latitude': getattr(photo_bunch, 'latitude', ''),
                'geo_longitude': getattr(photo_bunch, 'longitude', ''),
                'geo_accuracy': getattr(photo_bunch, 'accuracy', ''),
                }
        photo_data.update(geo_data)
        return photo_data

    def _add_tags(self, obj, tags):
        try:
            obj.tags.set(*[tag for tag in tags.split()])
        except KeyError:
            pass
        except:
            # \todo TBD: implements feeders: from 'getPhotos' and from 'getInfo'
            pass

    def _add_sizes(self, obj, photo, sizes):
        if sizes:
            for size in sizes['sizes']['size']:
                obj.sizes.create_from_json(photo=obj, size=size)
        else:
            for key, size in FLICKR_PHOTO_SIZES.items():
                url_suffix = size.get('url_suffix', None)
                if url_suffix and getattr(photo, 'url_%s' % url_suffix, None):
                    size_data = {
                            'label' : key,
                            'width' : getattr(photo, 'width_%s' % url_suffix, None),
                            'height' : getattr(photo, 'height_%s' % url_suffix, None),
                            'source' : getattr(photo, 'url_%s' % url_suffix, None),
                            }
                    obj.sizes.create_from_json(photo=obj, size=size_data)

    def create_from_json(self, flickr_user, photo, info=None, sizes=None, exif=None, geo=None, **kwargs):
        """Create a record for flickr_user"""
        photo_data = self._prepare_data(flickr_user=flickr_user, photo=photo, info=info, exif=exif, geo=geo, **kwargs)
        tags = photo_data.pop('tags')
        obj = self.create(**dict(photo_data.items() + kwargs.items()))
        self._add_tags(obj, tags)
        self._add_sizes(obj, photo, sizes)
        return obj

    def update_from_json(self, flickr_user, flickr_id, photo, info=None, sizes=None, exif=None, geo=None, **kwargs):
        """Update a record with flickr_id"""
        update_tags = kwargs.pop('update_tags', False)
        photo_data = self._prepare_data(photo=photo, flickr_user=flickr_user, info=info, exif=exif, geo=geo, **kwargs)
        tags = photo_data.pop('tags')
        result = self.filter(flickr_id=flickr_id).update(**dict(photo_data.items() + kwargs.items()))
        if result == 1:
            obj = self.get(flickr_id=flickr_id)
            if update_tags:
                obj.tags.clear()
                self._add_tags(obj, tags)
            if kwargs.get('update_sizes', False):
                obj.sizes.clear()  # Delete all sizes or only update them?
                self._add_sizes(obj, photo, sizes)
        return result

    def create_or_update_from_json(self, flickr_user, info, sizes=None, exif=None, geo=None, **kwargs):
        """Pretty self explanatory"""


class Photo(FlickrModel):

    """http://www.flickr.com/services/api/explore/flickr.photos.getInfo"""

    server = models.PositiveSmallIntegerField()
    farm = models.PositiveSmallIntegerField()
    secret = models.CharField(max_length=10)
    originalsecret = models.CharField(max_length=10)
    originalformat = models.CharField(max_length=4, null=True, blank=True)

    title = models.CharField(max_length=255, null=True, blank=True)
    description = models.TextField(null=True, blank=True)

    date_posted = models.DateTimeField(null=True, blank=True)
    date_taken = models.DateTimeField(null=True, blank=True)
    date_taken_granularity = models.PositiveSmallIntegerField(null=True, blank=True)
    date_updated = models.DateTimeField(null=True, blank=True)

    url_page = models.URLField(max_length=255, null=True, blank=True)
    tags = TaggableManager(blank=True)

    slug = models.SlugField(max_length=255, null=True, blank=True)

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
        return reverse('flickr_photo', args=[self.flickr_id, ])

    @property
    def flickr_page_url(self):
        return '%s%s/' % (self.user.flickr_page_url, self.flickr_id)

    """because 'Model.get_previous_by_FOO(**kwargs) For every DateField and DateTimeField that does not have null=True'"""
    def get_next_by_date_posted(self):
        try:
            return Photo.objects.filter(date_posted__gte=self.date_posted).exclude(flickr_id=self.flickr_id).order_by('date_posted', 'date_taken')[:1].get()
        except:
            pass

    def get_next_public_by_date_posted(self):
        try:
            return Photo.objects.public().filter(date_posted__gte=self.date_posted).exclude(flickr_id=self.flickr_id).order_by('date_posted', 'date_taken')[:1].get()
        except:
            pass

    def get_previous_by_date_posted(self):
        try:
            return Photo.objects.filter(date_posted__lte=self.date_posted).exclude(flickr_id=self.flickr_id).order_by('-date_posted', '-date_taken')[:1].get()
        except:
            pass

    def get_previous_public_by_date_posted(self):
        try:
            return Photo.objects.public().filter(date_posted__lte=self.date_posted).exclude(flickr_id=self.flickr_id).order_by('-date_posted', '-date_taken')[:1].get()
        except:
            pass

    """shortcuts - bringing some sanity"""
    def get_next(self):
        return self.get_next_public_by_date_posted()

    def get_prev(self):
        return self.get_previous_public_by_date_posted()

    def get_next_by_date_taken(self):
        try:
            return Photo.objects.filter(date_taken__gte=self.date_taken)[:1].get()
        except:
            pass

    def get_previous_by_date_taken(self):
        try:
            return Photo.objects.filter(date_taken__lte=self.date_taken)[:1].get()
        except:
            pass

    def get_next_in_photoset(self, photoset):
        if not hasattr(self, '_next_in_ps%s' % photoset.flickr_id):
            photo = None
            try:
                if photoset.photos.filter(flickr_id=self.flickr_id).exists():
                    photo = photoset.photos.visible().filter(date_posted__gte=self.date_posted).exclude(flickr_id=self.flickr_id).order_by('date_posted', 'date_taken')[:1].get()
                    print photo
            except:
                pass
            setattr(self, '_next_in_ps%s' % photoset.flickr_id, photo)
        return getattr(self, '_next_in_ps%s' % photoset.flickr_id)

    def get_previous_in_photoset(self, photoset):
        if not hasattr(self, '_previous_in_ps%s' % photoset.flickr_id):
            photo = None
            try:
                if photoset.photos.filter(flickr_id=self.flickr_id).exists():
                    photo = photoset.photos.visible().filter(date_posted__lte=self.date_posted).exclude(flickr_id=self.flickr_id).order_by('-date_posted', '-date_taken')[:1].get()
            except:
                pass
            setattr(self, '_previous_in_ps%s' % photoset.flickr_id, photo)
        return getattr(self, '_previous_in_ps%s' % photoset.flickr_id)


class PhotoSizeDataManager(models.Manager):
    def _prepare_data(self, size, photo=None, **kwargs):
        size_data = bunchify(size)
        data = {'size': FLICKR_PHOTO_SIZES[size_data.label]['label'],
                'width': size_data.width,
                'height': size_data.height,
                'source': size_data.source,
                'url': unslash(getattr(size_data, 'url', '')),
              }
        if photo:
            data['photo'] = photo
        return data

    def create_from_json(self, photo, size, **kwargs):
        """Create a record for photo size data"""
        photosize_data = self._prepare_data(photo=photo, size=size, **kwargs)
        obj = self.create(**dict(photosize_data.items() + kwargs.items()))
        return obj

    def update_from_json(self, photosize_id, size, **kwargs):
        photosize_data = self._prepare_data(size=size, **kwargs)
        result = self.filter(id=photosize_id).update(**dict(photosize_data.items()) + kwargs.items())
        return result


class PhotoSizeData(models.Model):
    photo = models.ForeignKey(Photo, related_name='sizes')
    size = models.CharField(max_length=10, choices=[(v['label'], k) for k, v in FLICKR_PHOTO_SIZES.iteritems()])
    width = models.PositiveIntegerField(null=True, blank=True)
    height = models.PositiveIntegerField(null=True, blank=True)
    source = models.URLField(null=True, blank=True)
    url = models.URLField(null=True, blank=True)

    objects = PhotoSizeDataManager()

    class Meta:
        unique_together = (('photo', 'size'),)


""" Dynamic addition of properties to access photo sizes information (stored in photo model fields) """


def attrproperty(getter_function):
    class _Object(object):

        def __init__(self, obj):
            self.obj = obj

        def __getattr__(self, attr):
            return getter_function(self.obj, attr)
    return property(_Object)


class PhotoSize(object):
    _source = None
    _url = None

    label = None
    secret_field = None
    format_field = None
    source_suffix = None
    url_suffix = None
    source_append = ''

    object = None

    def __init__(self, photo, **kwargs):
        self.photo = photo
        for key, value in kwargs.iteritems():
            setattr(self, key, value)

        self.secret = getattr(self.photo, self.secret_field)
        self.format = 'jpg' if not self.format_field else getattr(self.photo, self.format_field)

    @classmethod
    def as_property(cls, size):
        data_dict = {'label': size['label'],
                    'secret_field': size.get('secret_field', 'secret'),
                    'format_field': size.get('format_field', None),
                    'source_suffix': size.get('source_suffix', None),
                    'url_suffix': size.get('url_suffix', None),
                    'source_append' : size.get('source_append', ''),
                    }

        def func(self, attr):
            obj = getattr(self, '_%s' % data_dict['label'], None)
            if not obj:
                obj = PhotoSize(self, **data_dict)
                setattr(self, '_%s' % data_dict['label'], obj)
            return getattr(obj, attr)
        return func

    def _get_object(self):
        if not self.object:
            self.object = self.photo.sizes.filter(size=self.label).get()
        return self.object

    def _get_source(self):
        if not self._source:
            if self.object:
                self._source = self.object.source
            if not self._source:
                self._source = build_photo_source(self.photo.farm, self.photo.server, self.photo.flickr_id, self.secret, self.source_suffix, self.format, self.source_append)
        return self._source
    source = property(_get_source)

    def _get_url(self):
        if not self._url:
            if self.object:
                self._url = self.object.url
            if not self._url:
                self._url = '%s%s/sizes/%s/' % (self.photo.user.flickr_page_url, self.photo.flickr_id, self.url_suffix)
        return self._url
    url = property(_get_url)

    @property
    def width(self):
        if self.object:
            return self.object.width
        return None

    @property
    def height(self):
        if self.object:
            return self.object.height
        return None

for key, size in FLICKR_PHOTO_SIZES.items():
    label = size.get('label', None)
    setattr(Photo, label, attrproperty(PhotoSize.as_property(size=size)))
    """ Deprecation warning """
    for dato in ['source', 'url', 'width', 'height']:
        method_deprecated = 'photo.%s_%s' % (label, dato)
        method_suggested = 'photo.%s.%s' % (label, dato)

        def get_property(self, label=label, dato=dato):
            from warnings import warn
            string = "Accessing photo sizes properties through '%s' is deprecated. Use '%s' instead." % (method_deprecated, method_suggested)
            warn(string)
            return getattr(getattr(self, label), dato)

        def set_property(self, value, label=label, dato=dato):
            """
                We cannot do it this way because we don't already have
                a photo.id (not saved) and, if we save it, we get an
                exception when finishing creating call in PhotoManager::create_from_json

                if not self.id:
                    self.save()
                size_data, created = PhotoSizeData.objects.get_or_create(photo = self, size=label)
                size_data.dato = value
                size_data.save()
            """
            raise NotImplementedError
        setattr(Photo, '%s_%s' % (label, dato), property(get_property, set_property))


def thumb(self):
    return '<img src="%s"/>' % getattr(self, 'square_source')
thumb.allow_tags = True
setattr(Photo, 'thumbnail', thumb)


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

    def _prepare_data(self, info, photos, flickr_user, exif=None, geo=None):
        photoset = bunchify(info)
        photos = bunchify(photos['photoset']['photo'])

        data = {'flickr_id': photoset.id, 'server': photoset.server,
                  'secret': photoset.secret, 'farm': photoset.farm, 'primary': photoset.primary,
                  'title': photoset.title._content, 'description': photoset.description._content,
                  'date_posted': ts_to_dt(photoset.date_create, flickr_user.tzoffset), 'date_updated': ts_to_dt(photoset.date_update, flickr_user.tzoffset),
                  'photos': photos,
                  'last_sync': now(),
                  }
        if flickr_user:
            data['user'] = flickr_user
        return data

    def update_from_json(self, flickr_user, flickr_id, info, photos, update_photos=False, **kwargs):
        """Update a record with flickr_id"""
        photoset_data = self._prepare_data(info=info, photos=photos, flickr_user=flickr_user, **kwargs)
        photos = photoset_data.pop('photos')
        result = self.filter(flickr_id=flickr_id).update(**dict(photoset_data.items() + kwargs.items()))
        if result == 1 and update_photos:
            obj = self.get(flickr_id=flickr_id)
            obj.photos.clear()
            self._add_photos(obj, photos)
        return result

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
    primary = models.CharField(max_length=50, null=True, blank=True)  # #flickr id of primary photo

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
        return reverse('flickr_photoset', args=[self.flickr_id, ])

    @property
    def flickr_page_url(self):
        return '%ssets/%s/' % (self.user.flickr_page_url, self.flickr_id)

    def cover(self):
        try:
            return Photo.objects.get(flickr_id=self.primary)
        except Photo.DoesNotExist:
            try:
                return Photo.objects.filter(photoset__id__in=[self.id, ]).latest()
            except Photo.DoesNotExist:
                pass

    def thumbnail(self):
        if self.cover():
            return '<img src="%s"/>' % self.cover().square_source
    thumbnail.allow_tags = True


class CollectionManager(models.Manager):

    def _add_sets(self, obj, sets):
        """add sets that are present in our database"""
        flickr_sets = PhotoSet.objects.filter(flickr_id__in=[s.id for s in sets])
        obj.sets.add(*[s.id for s in flickr_sets])

    def _prepare_data(self, info, flickr_user, parent=None):
        col = bunchify(info)
        data = {'flickr_id': col.id,
                'title': col.title, 'description': col.description,
                'parent': parent, 'last_sync': now(), 'icon': col.iconlarge,
                }
        if flickr_user:
            data['user'] = flickr_user
        if 'date_create' in col.keys():
            data['date_created'] = ts_to_dt(col.date_create, flickr_user.tzoffset)
        if 'set' in col.keys():
            data['sets'] = col.set
        if 'collection' in col.keys():
            data['collections'] = col.collection
        return data

    def create_obj(self, info, parent=None, flickr_user=None, **kwargs):
        data = self._prepare_data(info, parent, flickr_user)
        sets_data = cols_data = None
        if 'sets' in data.keys():
            sets_data = data.pop('sets')
        if 'collections' in data.keys():
            cols_data = data.pop('collections')
        if kwargs.pop('update', False):
            obj = self.filter(flickr_id=data['flickr_id']).update(**dict(data.items() + kwargs.items()))
            if obj:  # #filter().update() didn't return object
                obj = self.get(flickr_id=data['flickr_id'])
            else:
                obj = self.create(**dict(data.items() + kwargs.items()))
        else:
            obj = self.create(**dict(data.items() + kwargs.items()))
        if sets_data:
            self._add_sets(obj, sets_data)
        return obj, cols_data

    def create_or_update_obj(self, info, parent=None, flickr_user=None, **kwargs):
        return self.create_obj(info, parent, flickr_user, update=True, **kwargs)

    def create_recursive(self, col, parent=None, flickr_user=None, **kwargs):
        update_flag = kwargs.pop('update', False)
        if update_flag:
            obj, children = self.create_or_update_obj(col, parent, flickr_user)
        else:
            obj, children = self.create_obj(col, parent, flickr_user)
        if children != None:
            parent = obj
            for child in children:
                if update_flag:
                    self.create_or_update_obj(child, parent, flickr_user)
                else:
                    self.create_recursive(child, parent, flickr_user)
        return True

    def create_from_usertree_json(self, flickr_user, tree, **kwargs):
        collections = tree['collections']['collection']
        for col in collections:
            self.create_recursive(col, parent=None, flickr_user=flickr_user, **kwargs)
        return True

    def create_or_update_from_usertree_json(self, flickr_user, tree, **kwargs):
        return self.create_from_usertree_json(flickr_user, tree, update=True, **kwargs)


class Collection(FlickrModel):

    parent = models.ForeignKey('self', null=True)
    title = models.CharField(max_length=200)
    description = models.TextField(null=True, blank=True)
    icon = models.URLField(max_length=255, null=True, blank=True)
    sets = models.ManyToManyField(PhotoSet, null=True)
    date_created = models.DateTimeField(null=True, blank=True)

    objects = CollectionManager()

    class Meta:
        ordering = ('-date_created',)
        get_latest_by = 'date_created'

    def __unicode__(self):
        return u'%s' % self.title

    @property
    def flickr_page_url(self):
        return '%scollections/%s/' % (self.user.flickr_page_url, (self.flickr_id.split('-')[-1]))

    def thumbnail(self):
        return '<img src="%s"/>' % self.icon.replace('_l.', '_s.')
    thumbnail.allow_tags = True


class JsonCache(models.Model):

    flickr_id = models.CharField(max_length=50, null=True, blank=True)
    info = models.TextField(null=True, blank=True)
    sizes = models.TextField(null=True, blank=True)
    exif = models.TextField(null=True, blank=True)
    geo = models.TextField(null=True, blank=True)
    exception = models.TextField(null=True, blank=True)
    added = models.DateTimeField(auto_now=True, auto_now_add=True)


class PhotoDownload(models.Model):

    def upload_path(self, filename):
        dirbase = getattr(settings, 'FLICKR_DOWNLOAD_DIRBASE', 'flickr')
        dirformat = getattr(settings, 'FLICKR_DOWNLOAD_DIRFORMAT', '%Y/%Y-%m')
        return '/'.join([dirbase, str(self.photo.date_posted.date().strftime(dirformat)), filename])

    photo = models.OneToOneField(Photo)
    url = models.URLField(max_length=255, null=True, blank=True)
    image_file = models.FileField(upload_to=upload_path, null=True, blank=True)
    size = models.CharField(max_length=10, choices=[(v['label'], k) for k, v in FLICKR_PHOTO_SIZES.iteritems()])
    errors = models.TextField(null=True, blank=True)
    date_downloaded = models.DateTimeField(auto_now=True, auto_now_add=True)

    def __unicode__(self):
        return u'%s' % str(self.photo)
