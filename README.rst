Django Flickr
=============

Django Flickr provides a mechanism to mirror user's flickr photos
into a local database.

Sources:
 * stable: https://bitbucket.org/zalew/django-flickr/

.. contents:: Table of Contents

Features
--------

This application replicates your Flickr photos database (currently photos
and photosets, collections comming soon) to Django models and provides
management commands to sync your Django app with your Flickr content.

Dependencies
------------

 * http://pypi.python.org/pypi/bunch/1.0.0 to ease up managing json data
 * https://github.com/alex/django-taggit for handling tags
 * https://github.com/feuervogel/django-taggit-templatetags (not obligatory really, but it's an awesome addition to taggit and the example view uses it) 

Installation
------------

From pypi_::

    $ pip install django-flickr

or clone from bitbucket_::

    $ hg clone https://bitbucket.org/zalew/django-flickr



Configuration
-------------

Add 'flickr' to your INSTALLED_APPS and syncdb

Go to 'Your apps' on Flickr and generate an API key for your app. Put those data in your settings.py::

    FLICKR_KEY = 'xxxxxxxxxxxx'
    FLICKR_SECRET = 'xxxxxxx'
    FLICKR_PERMS = 'read'

and add flickr.urls to your urls.py


Use cases
---------

1. Sync photos::

    $ ./manage.py flickr_sync [options]

   available options are::

    -i, --initial
                    Initial sync. For improved performance it assumpts db
                    flickr tables are empty and blindly hits create().
    -d DAYS, --days=DAYS
                    Sync photos from the last n days. Default is 1 day.
                    Useful for cron jobs.
    -u USER_ID, --user=USER_ID
                    Sync for a particular user. Default is 1 (in most
                    cases it's the admin and you're using it only for
                    yourself).
    --page=PAGE
                    Grab a specific portion of photos. To be used with
                    --per_page.
    --per_page=PER_PAGE
                    How many photos per page should we grab? Set low value
                    (10-50) for daily/weekly updates so there is less to
                    parse, set high value (200-500) for initial sync and
                    big updates so we hit flickr less.
    --force_update
                    If photo in db, override with new data.
    --photosets
                    Sync photosets (only photosets, no photos sync action
                    is run). Photos must be synced first. If photo from
                    photoset not in our db, it will be ommited.
    -t, --test
                    Test/simulate. Don't write results to db.

   How long does it take to sync?

   Initial sync of 850 photos took about 90 minutes on my production server. There are sleep() to prevent dropping us by Flickr, but they steal only 23s per 100 pictures. There are a few api calls per one picture (info, exif, sizes, etc.), so it takes a while.

2. Download photos (NYI, TODO)::

    $ ./manage.py flickr_download [options]

Bugs
----

The project is in early stages, expect bugs. Please report any issues.

Contributors
------------

- Jakub Zalewski http://zalew.net
- Javier García Sogo https://bitbucket.org/jgsogo


.. _pypi: http://pypi.python.org/pypi/django-flickr
.. _bitbucket: https://bitbucket.org/zalew/django-flickr
