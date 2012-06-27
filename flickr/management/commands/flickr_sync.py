#!/usr/bin/env python
# encoding: utf-8
from django.contrib.auth.models import User
from django.core.management.base import CommandError
from flickr.management.commands import FlickrCommand
from flickr.models import FlickrUser, Photo, JsonCache, PhotoSet, Collection
from flickr.shortcuts import get_all_photos, get_photosets_json, \
    get_photoset_photos_json, get_user_json, get_collections_tree_json, \
    get_photo_exif_json, get_photo_sizes_json, get_photo_info_json, get_photo_geo_json
from optparse import make_option
import datetime
import time


class Command(FlickrCommand):

    help_text = 'Django-Flickr\n\nRun "./manage.py flickr_sync --help" for details, \nor rtfm at http://bitbucket.org/zalew/django-flickr/ \n\n'

    option_list = FlickrCommand.option_list + (

        make_option('--user', '-u', action='store', dest='user_id', default=1,
            help='Sync for a particular user. Default is 1 (in most cases it\'s the admin and you\'re using it only for yourself).'),

        # Elements to sync

        make_option('--info', '-i', action='store_true', dest='info', default=False,
            help='Fetch info for photos. It will take a long time to sync as it needs to fetch Flickr data for every photo separately.'),

        make_option('--exif', '-e', action='store_true', dest='exif', default=False,
            help='Fetch exif for photos. It will take a long time to sync as it needs to fetch Flickr data for every photo separately.'),

        make_option('--sizes', '-s', action='store_true', dest='sizes', default=False,
            help='Fetch sizes details for photos. It is not needed, sizes can be obtained dynanmically. \
It will take a long time as it needs to fetch Flickr data for every photo separately. '),

        make_option('--geo', '-g', action='store_true', dest='geo', default=False,
            help='Fetch geo data for photos. It will take a long time as it needs to fetch Flickr data for every photo separately.'),

        make_option('--photosets', '-p', action='store_true', dest='photosets', default=False,
            help='Sync photosets. Photos must be synced first. If photo from photoset not in our db, it will be ommited.'),

        make_option('--collections', '-c', action='store_true', dest='collections', default=False,
            help='Sync collections. Photos and sets must be synced first.'),

        make_option('--no-photos', action='store_true', dest='no_photos', default=False,
            help='Don\'t sync photos.'),

        # Range to sync

        make_option('--days', '-d', action='store', dest='days', default=None,
            help='Sync photos from the last n days.'),

        make_option('--page', action='store', dest='page', default=None,
            help='Grab a specific portion of photos. To be used with --per_page.'),

        make_option('--per-page', action='store', dest='per_page', default=20,
            help='How many photos per page should we grab? Set low value (10-50) for daily/weekly updates so there is less to parse,\n\
set high value (200-500) for initial sync and big updates so we hit flickr less.'),

        make_option('--ils', action='store_true', dest='ils', default=False,
            help='Ignore last_sync.'),

        # Other

        make_option('--initial', action='store_true', dest='initial', default=None,
            help='It assumpts db flickr tables are empty and blindly hits create().'),

        make_option('--test', '-t', action='store_true', dest='test', default=False,
            help='Test/simulate. Don\'t write results to db.'),

        )

    def handle(self, *args, **options):
        super(Command, self).handle(*args, **options)
        t1 = time.time()

        """default behavior: sync pics and user info"""
        self.user_info(**options)
        if not options.get('no_photos', False):
            self.user_photos(**options)

        if options.get('photosets'):
            self.user_photosets(**options)

        if options.get('collections'):
            self.user_collections(**options)

        if not options.get('test', False):
            self.flickr_user.bump()  # #bump last_sync

        t2 = time.time()
        self.v('Exec time: ' + str(round(t2 - t1)), 0)
        return 'Sync end'

    def user_info(self, **options):
        flickr_user = self.flickr_user
        self.v('Syncing user info', 0)
        self.v('- getting user info for %s...' % flickr_user.user, 1)
        info = get_user_json(nsid=flickr_user.nsid, token=flickr_user.token)
        length = len(info)
        if length > 0:
            self.v('- got user info, it might take a while...', 1)
            if not options.get('test', False):
                FlickrUser.objects.update_from_json(pk=flickr_user.pk, info=info)
                self.flickr_user = FlickrUser.objects.get(pk=flickr_user.pk)
            else:
                self.v('-- got data for user', 1)
        self.v('COMPLETE: user info sync', 0)

    def user_photos(self, **options):
        flickr_user = self.flickr_user
        self.v('Syncing user photos', 0)
        self.v('- getting user photos list...', 1)
        page = options.get('page')
        per_page = options.get('per_page')
        min_upload_date = None
        if options.get('days'):
            days = int(options.get('days'))
            min_upload_date = (datetime.date.today() - datetime.timedelta(days)).isoformat()
        else:
            self.v('- fetching since last sync', 1)
            self.v('  (depending on the number of photos to sync it can take a while, be patient)', 1)
            self.v('  contacting Flickr...', 1)
            if not options.get('ils'):
                min_upload_date = flickr_user.last_sync
        photos = get_all_photos(nsid=flickr_user.nsid, token=flickr_user.token,
                        page=page, per_page=per_page, min_upload_date=min_upload_date)
        length = len(photos)
        if length > 0:
            self.v('- got %d photos, it might take a while...' % length, 1)
            i = 0
            for photo in photos:
                info = sizes = exif = geo = None
                self.v('- processing photo #%s "%s"' % (photo.id, photo.title), 2)
                try:
                    if options.get('info'):
                        self.v(' - fetching info', 2)
                        info = get_photo_info_json(photo_id=photo.id, token=flickr_user.token)
                    if options.get('sizes'):
                        self.v(' - fetching sizes', 2)
                        sizes = get_photo_sizes_json(photo_id=photo.id, token=flickr_user.token)
                    if options.get('exif'):
                        self.v(' - fetching exif', 2)
                        exif = get_photo_exif_json(photo_id=photo.id, token=flickr_user.token)
                    if options.get('geo'):
                        self.v(' - fetching geo', 2)
                        geo = get_photo_geo_json(photo_id=photo.id, token=flickr_user.token)
                    #info, sizes, exif, geo = get_photo_details_jsons(photo_id=photo.id, token=flickr_user.token)
                    if not options.get('test', False):
                        if options.get('initial', False):
                            #blindly create for initial sync (assumpts table is empty)
                            self.v(' - inserting to db', 2)
                            Photo.objects.create_from_json(flickr_user=flickr_user, photo=photo, info=info, sizes=sizes, exif=exif, geo=geo)
                        else:
                            if not Photo.objects.filter(flickr_id=photo.id):
                                self.v(' - inserting to db', 2)
                                Photo.objects.create_from_json(flickr_user=flickr_user, photo=photo, info=info, sizes=sizes, exif=exif, geo=geo)
                            else:
                                self.v(' - updating db', 2)
                                Photo.objects.update_from_json(flickr_id=photo.id, photo=photo, info=info, sizes=sizes, exif=exif, geo=geo, update_tags=options.get('update_tags', False))
                    else:
                        self.v(' - it\'s a test, so not writing to db', 2)
                except Exception as e:
                    self.v('- ERR failing silently exception "%s"' % (e), 1)
                    # in case sth got wrong with a data set, let's log all the data to db and not break the ongoing process
                    try:
                        JsonCache.objects.create(flickr_id=photo.id, photo=photo, info=info, sizes=sizes, exif=exif, geo=geo, exception=e)
                    except Exception as e2:
                        #whoa sth is really messed up
                        JsonCache.objects.create(flickr_id=photo.id, exception=e2)
                i += 1
                if i % 10 == 0:
                    self.v('- %d photos processed, %d to go' % (i, length - i), 1)
                    time.sleep(2)  # #so we don't get our connections dropped by flickr api'
                if i % 100 == 0:
                    time.sleep(3)
        else:
            self.v('- nothing to sync', 0)
        self.v('COMPLETE: user photos sync', 0)

    def user_photosets(self, **options):
        flickr_user = self.flickr_user
        self.v('Syncing photosets', 0)
        self.v('- getting user photosets list...', 1)
        sets = get_photosets_json(nsid=flickr_user.nsid, token=flickr_user.token).photosets.photoset
        length = len(sets)
        if length > 0:
            self.v('- got %d photosets, fetching photos, it might take a while...' % length, 1)
            time.sleep(1)
            i = 0
            for s in sets:
                photos = get_photoset_photos_json(photoset_id=s.id, token=flickr_user.token)
                if not options.get('test', False):
                    if options.get('initial', False):
                        PhotoSet.objects.create_from_json(flickr_user=flickr_user, info=s, photos=photos)
                    else:
                        if not PhotoSet.objects.filter(flickr_id=s.id):
                            PhotoSet.objects.create_from_json(flickr_user=flickr_user, info=s, photos=photos)
                        else:
                            PhotoSet.objects.update_from_json(flickr_id=s.id, info=s, photos=photos, update_photos=options.get('update_photos', False))
                i += 1
                if i % 10 == 0:
                    self.v('- %d photosets fetched, %d to go' % (i, length - i), 1)
                    time.sleep(2)  # #so we don't get our connections dropped by flickr api'
        else:
            self.v('- nothing to sync', 1)
        self.v('COMPLETE: user photosets sync', 0)

    def user_collections(self, **options):
        flickr_user = self.flickr_user
        self.v('Syncing collections', 0)
        tree = get_collections_tree_json(nsid=flickr_user.nsid, token=flickr_user.token)
        length = len(tree)
        if length > 0:
            self.v('- got %d collections in root of tree for user' % length, 1)
            if not options.get('test', False):
                    if options.get('initial', False):
                        Collection.objects.create_from_usertree_json(flickr_user, tree)
                    else:
                        Collection.objects.create_or_update_from_usertree_json(flickr_user, tree)
        else:
            self.v('- nothing to sync', 1)
        self.v('COMPLETE: user collections sync', 0)
