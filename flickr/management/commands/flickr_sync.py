#!/usr/bin/env python
# encoding: utf-8
from django.conf import settings
from django.contrib.auth.models import User
from django.core.management.base import BaseCommand, CommandError
from flickr.api import FlickrApi
from flickr.models import FlickrUser, Photo, JsonCache, PhotoSet
from flickr.shortcuts import get_all_photos, get_photo_details_jsons,\
    get_photosets_json, get_photoset_photos_json, get_user_json
from optparse import make_option
import datetime
import time


class Command(BaseCommand):
    
    help_text = 'Django-Flickr\n\nRun "./manage.py flickr_sync --help" for details, \nor rtfm at http://bitbucket.org/zalew/django-flickr/ \n\n'
    
    option_list = BaseCommand.option_list + (
        
        make_option('--initial', '-i', action='store_true', dest='initial', default=None,
            help='Initial sync. For improved performance it assumpts db flickr tables are empty and blindly hits create().'),
        
        make_option('--days', '-d', action='store', dest='days', default=None,
            help='Sync photos from the last n days. Useful for cron jobs.'),       
                
        make_option('--user', '-u', action='store', dest='user_id', default=1,
            help='Sync for a particular user. Default is 1 (in most cases it\'s the admin and you\'re using it only for yourself).'),
                                             
        make_option('--page', action='store', dest='page', default=None,
            help='Grab a specific portion of photos. To be used with --per_page.'), 
                                                  
        make_option('--per_page', action='store', dest='per_page', default=20,
            help='How many photos per page should we grab? Set low value (10-50) for daily/weekly updates so there is less to parse,\n\
set high value (200-500) for initial sync and big updates so we hit flickr less.'),                                       
                                             
        make_option('--force_update', action='store_true', dest='force_update', default=False,
            help='If photo in db, override with new data.'),
        
        make_option('--photosets', action='store_true', dest='photosets', default=False,
            help='Sync photosets (only photosets, no photos sync action is run). Photos must be synced first. If photo from photoset not in our db, it will be ommited.'),
               
        make_option('--photos', action='store_true', dest='photos', default=False,
            help='Sync photos (only photos, no photosets sync action is run).'),

        make_option('--update_photos', action='store_true', dest='update_photos', default=False,
            help='Update photos when updating a photoset.'),

        make_option('--update_tags', action='store_true', dest='update_tags', default=False,
            help='Update tags when updating a photo.'),
    
        make_option('--test', '-t', action='store_true', dest='test', default=False,
            help='Test/simulate. Don\'t write results to db.'),         
         
        )
        
        
    def __init__(self):
        super(Command, self).__init__()
                
        self.FLICKR_KEY = getattr(settings, 'FLICKR_KEY', None)
        if not self.FLICKR_KEY:
            raise CommandError, 'No FLICKR_KEY in settings. %s' % self.help_text
        self.FLICKR_SECRET = getattr(settings, 'FLICKR_SECRET', None)
        if not self.FLICKR_SECRET:
            raise CommandError, 'No FLICKR_SECRET in settings. %s' % self.help_text
        self.api = FlickrApi(self.FLICKR_KEY, self.FLICKR_SECRET)
    
    
    def handle(self, *args, **options):
        t1 = time.time()
        user_id = options.get('user_id')
        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            raise Exception, 'User with id %d does not exist' % int(user_id)
        try:
            self.flickr_user = FlickrUser.objects.get(user=user)
            self.api.token = self.flickr_user.token
        except FlickrUser.DoesNotExist:
            raise CommandError, 'Flickr not authenticated for user %s. %s' % (str(user), self.help_text)
        
        if options.get('photosets'):
            if options.get('verbosity') > 0:
                print 'Syncing photosets'
            self.user_photosets(**options)
            self.flickr_user.save() # bump last_sync
        elif options.get('photos'):
            if options.get('verbosity') > 0:
                print 'Syncing photos'
            self.user_photos(**options)
            self.flickr_user.save() # bump last_sync
        else:
            """default behavior: sync pics newer than the newest and user info"""
            if options.get('verbosity') > 0:
                print 'Syncing default'
            self.user_photos(**options)
            self.user_info(**options) # this already bumps last_sync
            
        t2 = time.time()
        print 'Exec time: '+str(round(t2-t1))
        return 'Sync end'
    
    
    def user_info(self, **options):
        flickr_user = self.flickr_user
        print 'BEGIN: user info sync'
        print '- getting user info for %s...' % flickr_user.user
        info = get_user_json(nsid=flickr_user.nsid, token=flickr_user.token)
        length = len(info)
        if length > 0:
            print '- got user info, it might take a while...'
            if not options.get('test', False):
                FlickrUser.objects.update_from_json(pk=flickr_user.pk, info=info)
            else:
                print '-- got data for user'
        print 'COMPLETE: user info sync'
    
    
    def user_photos(self, **options):        
        flickr_user = self.flickr_user
        print 'BEGIN: user photos sync'
        print '- getting user photos list...'
        page = options.get('page')
        per_page = options.get('per_page')
        min_upload_date = None
        if options.get('days'):
            days = int(options.get('days'))
            min_upload_date = (datetime.date.today() - datetime.timedelta(days)).isoformat()
        else:
            try:
                if options.get('verbosity') > 1:
                    print 'fetching since last sync'
                min_upload_date = flickr_user.last_sync
            except:
                pass
        photos = get_all_photos(nsid=flickr_user.nsid, token=flickr_user.token, 
                        page=page, per_page=per_page, min_upload_date=min_upload_date)
        length = len(photos)
        if length > 0:
            print '- got %d photos, fetching info, it might take a while...' % length
            time.sleep(3)
            i = 0
            for photo in photos:
                try:
                    if options.get('verbosity') > 1:
                        print 'fetching info for photo #%s "%s"' % (photo.id, photo.title)
                    info, sizes, exif, geo = get_photo_details_jsons(photo_id=photo.id, token=flickr_user.token)
                    if not options.get('test', False):
                        if options.get('initial', False):
                            #blindly create for initial sync (assumpts table is empty)
                            if options.get('verbosity') > 1:
                                print 'inserting photo #%s "%s"' % (photo.id, photo.title)
                            Photo.objects.create_from_json(flickr_user=flickr_user, info=info, sizes=sizes, exif=exif, geo=geo)
                        else:                            
                            if not Photo.objects.filter(flickr_id=photo.id):
                                if options.get('verbosity') > 1:
                                    print 'inserting photo #%s "%s"' % (photo.id, photo.title)
                                Photo.objects.create_from_json(flickr_user=flickr_user, info=info, sizes=sizes, exif=exif, geo=geo)
                            else:
                                if options.get('verbosity') > 1:
                                    print 'record found for photo #%s "%s"' % (photo.id, photo.title)
                                if options.get('force_update', False): 
                                    if options.get('verbosity') > 1:
                                        print 'updating photo #%s "%s"' % (photo.id, photo.title)                            
                                    Photo.objects.update_from_json(flickr_id=photo.id, info=info, sizes=sizes, exif=exif, geo=geo, update_tags=options.get('update_tags', False))
                    else:
                        print '-- got data for photo #%s "%s"' % (photo.id, photo.title)
                except Exception as e:
                    if options.get('verbosity') > 1:
                        print 'ERR failing silently exception "%s"' % (e)
                    # in case sth got wrong with a data set, let's log all the data to db and not break the ongoing process
                    try:                
                        JsonCache.objects.create(flickr_id=photo.id, info=info, sizes=sizes, exif=exif, geo=geo, exception=e)
                    except Exception as e2:
                        #whoa sth is really messed up
                        JsonCache.objects.create(flickr_id=photo.id, exception=e2)
                i += 1
                if i % 10 == 0:
                    print '- %d photos info fetched, %d to go'  % (i, length-i)
                    time.sleep(2) #so we don't get our connections dropped by flickr api'
                if i % 100 == 0:
                    time.sleep(3)
        else:
            print '- nothing to sync'
        print 'COMPLETE: user photos sync'        
        
    
    def user_photosets(self, **options):
        flickr_user = self.flickr_user
       
        print 'BEGIN: user photosets sync'
        print '- getting user photosets list...'
        sets = get_photosets_json(nsid=flickr_user.nsid, token=flickr_user.token).photosets.photoset
        length = len(sets)
        if length > 0:
            print '- got %d photosets, fetching photos, it might take a while...' % length
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
                            if options.get('force_update', False):
                                PhotoSet.objects.update_from_json(flickr_id=s.id, info=s, photos=photos, update_photos=options.get('update_photos', False))
                i += 1
                if i % 10 == 0:
                    print '- %d photosets fetched, %d to go'  % (i, length-i)
                    time.sleep(2) #so we don't get our connections dropped by flickr api'
        else:
            print '- nothing to sync'
        print 'COMPLETE: user photosets sync'        

        
        
    
