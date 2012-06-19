#from __future__ import print_function
from django.conf import settings
from django.contrib.auth.models import User
from django.core.management.base import BaseCommand, CommandError
from flickr.api import FlickrApi
from flickr.models import FlickrUser
import time
import sys


class Printer():
    """Print things to stdout on one line dynamically"""
    def __init__(self, data):
        sys.stdout.write("\r\x1b[K" + data.__str__())
        sys.stdout.flush()


class FlickrCommand(BaseCommand):

    def loader(self, i, total, message, errors_message=None):
        message = '%d%% [%d/%d] %s' % (int(round(float(i) / total * 100)), i, total, errors_message) + message
        self.v(message, 1, True)

    def v(self, message, level=1, inplace=False):
        if level <= self.verbosity:
            if inplace:
                Printer(message)
            else:
                print message

    def __init__(self):
        super(FlickrCommand, self).__init__()
        self.FLICKR_KEY = getattr(settings, 'FLICKR_KEY', None)
        if not self.FLICKR_KEY:
            raise CommandError, 'No FLICKR_KEY in settings. %s' % self.help_text
        self.FLICKR_SECRET = getattr(settings, 'FLICKR_SECRET', None)
        if not self.FLICKR_SECRET:
            raise CommandError, 'No FLICKR_SECRET in settings. %s' % self.help_text
        self.api = FlickrApi(self.FLICKR_KEY, self.FLICKR_SECRET)

    def handle(self, *args, **options):
        self.verbosity = options.get('verbosity')
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
