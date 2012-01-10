from bunch import bunchify
from django.conf import settings
from flickr.api import FlickrApi
from flickr.models import FlickrUser
import time

FLICKR_KEY = getattr(settings, 'FLICKR_KEY', None)
FLICKR_SECRET = getattr(settings, 'FLICKR_SECRET', None)


def get_token_for_user(user):
    try:
        fs = FlickrUser.objects.get(user=user)
        return fs.token                
    except FlickrUser.DoesNotExist:
        return None
    
    
def get_photos_json(nsid, token, page=1, per_page=500, min_upload_date=None):
    api = FlickrApi(FLICKR_KEY, FLICKR_SECRET, token)
    return bunchify(api.get(method='people.getPhotos', user_id=nsid, page=page, per_page=per_page, min_upload_date=min_upload_date))
    
    
def get_all_photos(nsid, token, page=None, per_page=None, min_upload_date=None):    
    data = get_photos_json(nsid, token, page, per_page, min_upload_date)
    user_photos = data.photos
    #per_page = user_photos.perpage
    #page = user_photos.page
    pages = user_photos.pages
    total = int(user_photos.total)
    photos = user_photos.photo
    if pages > 1 and not page:
        for page in range(2, pages+1):            
            time.sleep(1)
            data = get_photos_json(nsid, token, page, per_page)
            photos += data.photos.photo
    if not page and len(photos) != total:
        raise Exception, "Photos number don't match (%d != %d)" % (len(photos), total)
    return photos


def get_photo_details_jsons(photo_id, token):
    api = FlickrApi(FLICKR_KEY, FLICKR_SECRET, token)
    info  = api.get(method='photos.getInfo', photo_id=photo_id)
    time.sleep(1)
    sizes = api.get(method='photos.getSizes', photo_id=photo_id)
    time.sleep(1)
    exif  = api.get(method='photos.getExif', photo_id=photo_id)
    time.sleep(1)
    geo = None
    return info, sizes, exif, geo


def get_photosets_json(nsid, token):
    api = FlickrApi(FLICKR_KEY, FLICKR_SECRET, token)
    return bunchify(api.get(method='flickr.photosets.getList', user_id=nsid, page=1, per_page=500))
    
    
def get_photoset_photos_json(photoset_id, token):
    api = FlickrApi(FLICKR_KEY, FLICKR_SECRET, token)
    return bunchify(api.get(method='flickr.photosets.getPhotos', photoset_id=photoset_id))
    

