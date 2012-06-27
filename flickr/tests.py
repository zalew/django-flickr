#!/usr/bin/env python
# encoding: utf-8
from bunch import bunchify
from datetime import datetime
from django.contrib.auth.models import User
from django.test import TestCase
from django.test.client import Client
from flickr.flickr_spec import FLICKR_PHOTO_SIZES
from flickr.models import FlickrUser, Photo, PhotoSet, Collection
from flickr.tests_data import json_user, json_sizes, json_exif, json_geo, json_info, \
    json_photos_extras, json_photos, \
    json_set_info, json_set_photos, \
    json_collection_tree_user
from flickr.utils import unslash


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
        self.assertEqual(fu.ispro, json_user['person']['ispro'])
        self.assertEqual(fu.nsid, json_user['person']['nsid'])
        self.assertEqual(fu.realname, json_user['person']['realname']['_content'])
        self.assertEqual(fu.iconserver, json_user['person']['iconserver'])
        self.assertEqual(fu.iconfarm, json_user['person']['iconfarm'])
        self.assertEqual(fu.path_alias, json_user['person']['path_alias'])
        self.assertEqual(fu.profileurl, json_user['person']['profileurl']['_content'].replace('\\/', '/'))

    def test_photo_create(self):
        json_info = json_photos_extras['photos']['photo'][0]

        photo = Photo.objects.create_from_json(flickr_user=self.flickr_user, photo=json_info)  # #sizes=json_sizes, exif=json_exif)
        self.assertEqual(photo.flickr_id, json_info['id'])
        self.assertEqual(photo.title, json_info['title'])
        self.assertEqual(photo.server, json_info['server'])
        self.assertEqual(photo.farm, json_info['farm'])
        self.assertEqual(photo.secret, json_info['secret'])
        self.assertEqual(photo.originalsecret, json_info['originalsecret'])
        self.assertEqual(photo.ispublic, json_info['ispublic'])
        self.assertEqual(photo.isfriend, json_info['isfriend'])
        self.assertEqual(photo.isfamily, json_info['isfamily'])
        self.assertEqual(photo.date_posted, datetime.fromtimestamp(int(json_info['dateupload'])).strftime('%Y-%m-%d %H:%M:%S'))

        json_info = json_photos_extras['photos']['photo'][1]
        photo = Photo.objects.create_from_json(flickr_user=self.flickr_user, photo=json_info, exif=json_exif)
        self.assertEqual(photo.exif, str(json_exif))
        self.assertEqual(photo.exif_camera, json_exif['photo']['camera'])
        self.assertEqual(photo.exif_exposure, json_exif['photo']['exif'][3]['raw']['_content'].replace('\\/', '/'))
        self.assertEqual(photo.exif_aperture, json_exif['photo']['exif'][4]['clean']['_content'].replace('\\/', '/'))
        """
        self.assertEqual(photo.large_url, json_sizes['sizes']['size'][5]['url'].replace('\\/', '/'))
        self.assertEqual(photo.url_page, json_info['photo']['urls']['url'][0]['_content'].replace('\\/', '/'))
        """

    def test_photo_update(self):
        json_info = json_photos_extras['photos']['photo'][0]

        photo = Photo.objects.create_from_json(flickr_user=self.flickr_user, photo=json_info, sizes=json_sizes, exif=json_exif)
        self.assertEqual(photo.title, json_info['title'])
        new_title = 'whoa that is a new title here'
        json_info['title'] = new_title
        self.assertNotEqual(photo.title, json_info['title'])
        Photo.objects.update_from_json(flickr_id=photo.flickr_id, photo=json_info, sizes=json_sizes, exif=json_exif)
        obj = Photo.objects.get(flickr_id=photo.flickr_id)
        self.assertEqual(obj.title, new_title)

    def test_photoset(self):
        json_info = json_photos_extras['photos']['photo'][0]

        photo = Photo.objects.create_from_json(flickr_user=self.flickr_user, photo=json_info, sizes=json_sizes, exif=json_exif)

        photoset = PhotoSet.objects.create_from_json(flickr_user=self.flickr_user, info=json_set_info['photoset'], photos=json_set_photos)
        self.assertEqual(photoset.flickr_id, json_set_info['photoset']['id'])
        self.assertEqual(photoset.title, json_set_info['photoset']['title']['_content'])
        self.assertEqual(photoset.server, json_set_info['photoset']['server'])
        self.assertEqual(photoset.farm, json_set_info['photoset']['farm'])
        self.assertEqual(photoset.secret, json_set_info['photoset']['secret'])
        self.assertEqual(photoset.date_posted, datetime.fromtimestamp(int(json_set_info['photoset']['date_create'])).strftime('%Y-%m-%d %H:%M:%S'))
        photoset.photos.add(photo)
        self.assertEqual(photoset.photos.all().count(), 1)

    def test_collection(self):
        Collection.objects.create_from_usertree_json(flickr_user=self.flickr_user, tree=json_collection_tree_user)

        cols = Collection.objects.filter(user=self.flickr_user)
        #for col in cols:
        #    print col
        #    print col.sets.all()
        self.assertEqual(cols.count(), 9)
        cols = Collection.objects.filter(user=self.flickr_user).exclude(parent=None)
        self.assertEqual(cols.count(), 6)
        #cols = Collection.objects.filter(user=self.flickr_user).exclude(sets__isnull=True)
        #self.assertEqual(cols.count(), 7)

        Collection.objects.create_or_update_from_usertree_json(flickr_user=self.flickr_user, tree=json_collection_tree_user)
        cols = Collection.objects.filter(user=self.flickr_user)
        self.assertEqual(cols.count(), 9)
        cols = Collection.objects.filter(user=self.flickr_user).exclude(parent=None)
        self.assertEqual(cols.count(), 6)

    def test_dynamic_sizes(self):
        json_info_photo = json_photos_extras['photos']['photo'][0]
        json_info_data = json_info # json_photos_extras['photos']['photo'][0]
        tags = bunchify(json_info_photo)
        tags = tags.tags

        FlickrUser.objects.update_from_json(self.flickr_user.id, json_user)
        self.flickr_user = FlickrUser.objects.get(flickr_id=json_user['person']['id'])
        photo = Photo.objects.create_from_json(flickr_user=self.flickr_user, photo=json_info_photo, info=json_info_data, sizes=None, exif=json_exif)
        size_bunch = bunchify(json_sizes['sizes']['size'])
        for size in size_bunch:
            self.assertEqual(unslash(size.source), getattr(photo, FLICKR_PHOTO_SIZES[size.label]['label']).source)
            self.assertEqual(unslash(size.url), getattr(photo, FLICKR_PHOTO_SIZES[size.label]['label']).url)
        Photo.objects.update_from_json(flickr_id=photo.flickr_id, photo=json_info_photo, info=json_info, sizes=json_sizes, exif=json_exif)
        photo = Photo.objects.get(flickr_id=photo.flickr_id)
        self.assertEqual(photo.square_source, photo.square.source)
        self.assertEqual(photo.thumb_source, photo.thumb.source)
        self.assertEqual(photo.small_source, photo.small.source)
        self.assertEqual(photo.medium_source, photo.medium.source)
        self.assertEqual(photo.large_source, photo.large.source)
        self.assertEqual(photo.ori_source, photo.ori.source)


    def test_dynamic_sizes_dbhits(self):
        json_info = json_photos_extras['photos']['photo'][0]

        FlickrUser.objects.update_from_json(self.flickr_user.id, json_user)
        self.flickr_user = FlickrUser.objects.get(flickr_id=json_user['person']['id'])
        photo = Photo.objects.create_from_json(flickr_user=self.flickr_user, photo=json_info, sizes=None, exif=json_exif)
        photo = Photo.objects.get(flickr_id=photo.flickr_id)
        with self.assertNumQueries(1):
            size_bunch = bunchify(json_sizes['sizes']['size'])
            for size in size_bunch:
                self.assertEqual(unslash(size.source), getattr(photo, FLICKR_PHOTO_SIZES[size.label]['label']).source)
                self.assertEqual(unslash(size.url), getattr(photo, FLICKR_PHOTO_SIZES[size.label]['label']).url)
        Photo.objects.update_from_json(flickr_id=photo.flickr_id, photo=json_info, sizes=json_sizes, exif=json_exif)
        photo = Photo.objects.get(flickr_id=photo.flickr_id)
        with self.assertNumQueries(1):
            size_bunch = bunchify(json_sizes['sizes']['size'])
            for size in size_bunch:
                self.assertEqual(unslash(size.source), getattr(photo, FLICKR_PHOTO_SIZES[size.label]['label']).source)
                self.assertEqual(unslash(size.url), getattr(photo, FLICKR_PHOTO_SIZES[size.label]['label']).url)
