#!/usr/bin/env python
# encoding: utf-8
"""
Download all files from Flickr to disk (the ones in our synced DB'
"""
from django.core.files.base import ContentFile
from flickr.management.commands import FlickrCommand
from flickr.models import Photo, PhotoDownload
from optparse import make_option
import os
import time
import urllib2


class Command(FlickrCommand):

    help_text = 'Django-Flickr\n\nRun "./manage.py flickr_download --help" for details, \nor rtfm at http://bitbucket.org/zalew/django-flickr/ \n\n'

    option_list = FlickrCommand.option_list + (

        make_option('--user', '-u', action='store', dest='user_id', default=1,
            help='Sync for a particular user. Default is 1 (in most cases it\'s the admin and you\'re using it only for yourself).'),

        make_option('--all', '-a', action='store_true', dest='all', default=False,
            help='By default downloads only photos which have not been downloaded (default behavior). Use this option to (re)download all.'),

        make_option('--public', '-p', action='store_true', dest='public', default=False,
            help='Only public photos.'),

        make_option('--size', '-s', action='store_true', dest='size', default=None,
            help='Specify size for download (by default original for pro accounts and large for non-pro).'),

        make_option('--reset', '-r', action='store_true', dest='reset', default=False,
            help='Clear downloads db table. Does not affect your files.'),
        )

    def handle(self, *args, **options):
        super(Command, self).handle(*args, **options)

        t1 = time.time()

        if options.get('reset'):
            self.v('Deleting everything from PhotoDownload table (%d records).' % PhotoDownload.objects.count(), 0)
            [d.delete() for d in PhotoDownload.objects.all()]
            self.v('PhotoDownload table empty.', 0)
            return

        if options.get('public'):
            photos = Photo.objects.visible()
            self.v('Downloading public photos', 0)
        else:
            photos = Photo.objects.all()
            self.v('Downloading photos', 0)
        if not options.get('all'):
            photos = photos.exclude(id__in=[pd.photo.id for pd in PhotoDownload.objects.all()])
        length = len(photos)
        i = err = 0
        for photo in photos:
            i += 1
            message = '.' * i
            size = options.get('size')
            if not size:
                if self.flickr_user.ispro:
                    size = 'ori'
                else:
                    size = 'large'
            url = getattr(photo, size).source
            if not options.get('all'):
                dphoto = PhotoDownload.objects.create(photo=photo)
            else:
                dphoto, cr = PhotoDownload.objects.get_or_create(photo=photo)
            dphoto.url = url
            dphoto.size = size
            try:
                response = urllib2.urlopen(url)
                if response.headers['content-type'] in ['image/jpeg', 'image/jpg']:
                    content = response.read()
                    dphoto.image_file.save(os.path.basename(url), ContentFile(content), save=True)
                    #message += ' OK'
                else:
                    if response.url == 'http://l.yimg.com/g/images/photo_unavailable.gif':  # getcode() returns status 200
                        dphoto.errors = 'Size unavailable (' + url + ') ' + str(response.headers)
                        #TODO: what to do? what size fallback to?
                    else:
                        dphoto.errors = 'Content-type wrong. ' + str(response.headers)
                        #message += ' FAIL. check error log in db records\n'

            except Exception as e:
                #message += str(e)
                dphoto.errors = str(e)
                #message += 'FAIL. check error log in db records\n'
            dphoto.save()
            errors_message = ''
            if err > 0:
                errors_message = '(%d errors) ' % err
            message = '%d%% [%d/%d] %s' % (int(round(float(i) / length * 100)), i, length, errors_message) + message
            self.v(message, 1, True)

        t2 = time.time()
        self.v('Exec time: ' + str(round(t2 - t1)), 1)
        return 'Sync end'
