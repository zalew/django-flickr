#!/usr/bin/env python
# encoding: utf-8
"""
Download all files from Flickr to disk (the ones in our synced DB'
"""
from django.conf import settings
from django.contrib.auth.models import User
from django.core.files import File
from django.core.files.base import ContentFile
from django.core.management.base import BaseCommand, CommandError
from flickr.api import FlickrApi
from flickr.models import FlickrUser, Photo, PhotoDownload
from optparse import make_option
import os
import time
import urllib2



class Command(BaseCommand):
    
    help_text = 'Django-Flickr\n\nRun "./manage.py flickr_download --help" for details, \nor rtfm at http://bitbucket.org/zalew/django-flickr/ \n\n'
    
    option_list = BaseCommand.option_list + (
        
        make_option('--user', '-u', action='store', dest='user_id', default=1,
            help='Sync for a particular user. Default is 1 (in most cases it\'s the admin and you\'re using it only for yourself).'),
        
        make_option('--all', '-a', action='store_true', dest='all', default=False,
            help='By default downloads only photos which have not been downloaded (default behavior). Use this option to (re)download all.'),
                        
        make_option('--public', '-p', action='store_true', dest='public', default=False,
            help='Only public photos.'),
        
        make_option('--large', '-l', action='store_true', dest='large', default=False,
            help='Large instead of original (f.ex. for accounts with no access to original).'),
                                             
        make_option('--reset', '-r', action='store_true', dest='reset', default=False,
            help='Clear downloads db table. Does not affect your files.'),
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
        
        if options.get('reset'):
            print 'Deleting everything from PhotoDownload table (%d records).' % PhotoDownload.objects.count()
            [d.delete() for d in PhotoDownload.objects.all()]
            print 'PhotoDownload table empty.'        
            return
        
        if options.get('public'):
            photos = Photo.objects.visible()
        else:
            photos = Photo.objects.all()
        if not options.get('all'):
            photos = photos.exclude(id__in=[pd.photo.id for pd in PhotoDownload.objects.all()])
        for photo in photos:
            if options.get('large'):
                url = photo.large_source
            else:
                url = photo.ori_source
            if not options.get('all'):
                dphoto = PhotoDownload.objects.create(photo=photo)
            else:    
                dphoto, cr = PhotoDownload.objects.get_or_create(photo=photo)
            dphoto.url = url
            dphoto.ori = True
            if options.get('large'):
                dphoto.ori = False
            print u"Downloading '%s' (%s)" % (unicode(photo), url)
            try:
                response = urllib2.urlopen(url)
                if response.headers['content-type'] in ['image/jpeg', 'image/jpg']:
                    content = response.read()                    
                    dphoto.image_file.save(os.path.basename(url), ContentFile(content), save=True)
                    print 'OK\n'                    
                else:
                    dphoto.errors = 'Content-type wrong. ' + str(response.headers)
                    print 'FAIL. check error log in db records\n'
            except Exception as e:
                print str(e)
                dphoto.errors = str(e)
                print 'FAIL. check error log in db records\n'
            dphoto.save()           
                
        
        
        t2 = time.time()
        print 'Exec time: '+str(round(t2-t1))
        return 'Sync end'
    
        
