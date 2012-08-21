from bunch import bunchify
from django.conf import settings
from flickr.api import FlickrApi
from flickr.models import FlickrUser
import time


FLICKR_KEY = getattr(settings, 'FLICKR_KEY', None)
FLICKR_SECRET = getattr(settings, 'FLICKR_SECRET', None)

ALL_EXTRAS = 'description, license, date_upload, date_taken, owner_name, icon_server, original_format, last_update, geo, tags, machine_tags, o_dims, views, media, path_alias'

def get_token_for_user(user):
    try:
        fs = FlickrUser.objects.get(user=user)
        return fs.token
    except FlickrUser.DoesNotExist:
        return None


def get_photos_json(nsid, token, page=1, per_page=500, min_upload_date=None, extras=None):
    api = FlickrApi(FLICKR_KEY, FLICKR_SECRET, token)
    return bunchify(api.get(method='people.getPhotos', user_id=nsid, page=page, per_page=per_page, min_upload_date=min_upload_date, extras=extras))


def get_all_photos(nsid, token, page=None, per_page=None, min_upload_date=None, extras=None):
    data = get_photos_json(nsid, token, page, per_page, min_upload_date, extras)
    user_photos = data.photos
    #per_page = user_photos.perpage
    #page = user_photos.page
    pages = user_photos.pages
    total = int(user_photos.total)
    photos = user_photos.photo
    if pages > 1 and not page:
        for page in range(2, pages + 1):
            time.sleep(1)
            data = get_photos_json(nsid, token, page, per_page, extras=extras)
            photos += data.photos.photo
    if not page and len(photos) != total:
        raise Exception, "Photos number don't match (%d != %d)" % (len(photos), total)
    return photos


def get_photo_details_jsons(photo_id, token):
    api = FlickrApi(FLICKR_KEY, FLICKR_SECRET, token)
    info = api.get(method='photos.getInfo', photo_id=photo_id)
    time.sleep(1)
    sizes = api.get(method='photos.getSizes', photo_id=photo_id)
    time.sleep(1)
    exif = api.get(method='photos.getExif', photo_id=photo_id)
    time.sleep(1)
    geo = api.get(method='photos.geo.getLocation', photo_id=photo_id)
    return info, sizes, exif, geo


def get_photo_info_json(photo_id, token):
    api = FlickrApi(FLICKR_KEY, FLICKR_SECRET, token)
    info = api.get(method='photos.getInfo', photo_id=photo_id)
    return info


def get_photo_exif_json(photo_id, token):
    api = FlickrApi(FLICKR_KEY, FLICKR_SECRET, token)
    exif = api.get(method='photos.getExif', photo_id=photo_id)
    return exif


def get_photo_sizes_json(photo_id, token):
    api = FlickrApi(FLICKR_KEY, FLICKR_SECRET, token)
    sizes = api.get(method='photos.getSizes', photo_id=photo_id)
    return sizes

def get_photo_geo_json(photo_id, token):
    api = FlickrApi(FLICKR_KEY, FLICKR_SECRET, token)
    geo = api.get(method='photos.geo.getLocation', photo_id=photo_id)
    return geo


def get_photosets_json(nsid, token):
    api = FlickrApi(FLICKR_KEY, FLICKR_SECRET, token)
    return bunchify(api.get(method='flickr.photosets.getList', user_id=nsid, page=1, per_page=500))


def get_photoset_photos_json(photoset_id, token):
    api = FlickrApi(FLICKR_KEY, FLICKR_SECRET, token)
    return bunchify(api.get(method='flickr.photosets.getPhotos', photoset_id=photoset_id))


def get_user_json(nsid, token):
    api = FlickrApi(FLICKR_KEY, FLICKR_SECRET, token)
    return bunchify(api.get(method='flickr.people.getInfo', user_id=nsid))


def get_collections_tree_json(nsid, token):
    """tree for user or tree for collection"""
    api = FlickrApi(FLICKR_KEY, FLICKR_SECRET, token)
    return bunchify(api.get(method='collections.getTree', user_id=nsid))


def get_collection_info_json(collection_id, token):
    api = FlickrApi(FLICKR_KEY, FLICKR_SECRET, token)
    return bunchify(api.get(method='collections.getInfo', collection_id=collection_id))
