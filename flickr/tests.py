#!/usr/bin/env python
# encoding: utf-8
from datetime import datetime
from django.contrib.auth.models import User
from django.test import TestCase
from django.test.client import Client
from flickr.models import FlickrUser, Photo, PhotoSet
from flickr.tests_data import json_user, json_info, json_sizes, json_exif, \
    json_set_info, json_set_photos

    
class FlickrModelTests(TestCase):
        
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create(username='test', email='test@example.com')
        self.user.set_password('test')
        self.user.save()        
        self.flickr_user = FlickrUser.objects.create(user=self.user)
        self.user2 = User.objects.create(username='test2', email='test2@example.com')
        self.user2.set_password('test2')
        self.user2.save()
        self.flickr_user2 = FlickrUser.objects.create(user=self.user2)
    
    
    def test_user(self):
        FlickrUser.objects.update_from_json(self.flickr_user.id, json_user)
        fu = FlickrUser.objects.get(flickr_id=json_user['person']['id'])
        self.assertEqual(fu.flickr_id, json_user['person']['id'])
        self.assertEqual(fu.nsid, json_user['person']['nsid'])
        self.assertEqual(fu.realname, json_user['person']['realname']['_content'])
        self.assertEqual(fu.iconserver, json_user['person']['iconserver'])
        self.assertEqual(fu.iconfarm, json_user['person']['iconfarm'])
        self.assertEqual(fu.path_alias, json_user['person']['path_alias'])
        self.assertEqual(fu.profileurl, json_user['person']['profileurl']['_content'].replace('\\/','/'))
        
    
    def test_photo_create(self):        
        photo = Photo.objects.create_from_json(flickr_user=self.flickr_user, info=json_info, sizes=json_sizes, exif=json_exif)
        self.assertEqual(photo.flickr_id, json_info['photo']['id'])
        self.assertEqual(photo.title, json_info['photo']['title']['_content'])
        self.assertEqual(photo.server, json_info['photo']['server'])
        self.assertEqual(photo.farm, json_info['photo']['farm'])
        self.assertEqual(photo.secret, json_info['photo']['secret'])
        self.assertEqual(photo.originalsecret, json_info['photo']['originalsecret'])
        self.assertEqual(photo.ispublic, json_info['photo']['visibility']['ispublic'])
        self.assertEqual(photo.isfriend, json_info['photo']['visibility']['isfriend'])
        self.assertEqual(photo.isfamily, json_info['photo']['visibility']['isfamily'])
        self.assertEqual(photo.date_posted, datetime.fromtimestamp(int(json_info['photo']['dates']['posted'])).strftime('%Y-%m-%d %H:%M:%S') )
        self.assertEqual(photo.large_url, json_sizes['sizes']['size'][5]['url'].replace('\\/','/'))        
        self.assertEqual(photo.url_page, json_info['photo']['urls']['url'][0]['_content'].replace('\\/','/'))
        self.assertEqual(photo.exif, str(json_exif))
        self.assertEqual(photo.exif_camera, json_exif['photo']['camera'])
        self.assertEqual(photo.exif_exposure, json_exif['photo']['exif'][3]['raw']['_content'].replace('\\/','/'))
        self.assertEqual(photo.exif_aperture, json_exif['photo']['exif'][4]['clean']['_content'].replace('\\/','/'))
        
        
    def test_photo_update(self):
        photo = Photo.objects.create_from_json(flickr_user=self.flickr_user, info=json_info, sizes=json_sizes, exif=json_exif)
        self.assertEqual(photo.title, json_info['photo']['title']['_content'])
        new_title = 'whoa that is a new title here'
        json_info['photo']['title']['_content'] = new_title
        self.assertNotEqual(photo.title, json_info['photo']['title']['_content'])
        Photo.objects.update_from_json(flickr_id=photo.flickr_id, info=json_info, sizes=json_sizes, exif=json_exif)
        obj = Photo.objects.get(flickr_id=photo.flickr_id)
        self.assertEqual(obj.title, new_title)
        
        
    def test_photoset(self):
        
        photo = Photo.objects.create_from_json(flickr_user=self.flickr_user, info=json_info, sizes=json_sizes, exif=json_exif)
        
        photoset = PhotoSet.objects.create_from_json(flickr_user=self.flickr_user, info=json_set_info['photoset'], photos=json_set_photos)
        self.assertEqual(photoset.flickr_id, json_set_info['photoset']['id'])
        self.assertEqual(photoset.title, json_set_info['photoset']['title']['_content'])
        self.assertEqual(photoset.server, json_set_info['photoset']['server'])
        self.assertEqual(photoset.farm, json_set_info['photoset']['farm'])
        self.assertEqual(photoset.secret, json_set_info['photoset']['secret'])
        self.assertEqual(photoset.date_posted, datetime.fromtimestamp(int(json_set_info['photoset']['date_create'])).strftime('%Y-%m-%d %H:%M:%S'))
        self.assertEqual(photoset.photos.all().count(), 1)        
        
        
        


