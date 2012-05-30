.. _usage-commands:

Management Commands
===================
  

Sync photos database
---------------------

::

./manage.py flickr_sync [options]

::

  -i, --initial         Initial sync. For improved performance it assumpts db
                        flickr tables are empty and blindly hits create().
  -d DAYS, --days=DAYS  Sync photos from the last n days. Useful for cron
                        jobs.
  -u USER_ID, --user=USER_ID
                        Sync for a particular user. Default is 1 (in most
                        cases it's the admin and you're using it only for
                        yourself).
  --page=PAGE           Grab a specific portion of photos. To be used with
                        --per_page.
  --per_page=PER_PAGE   How many photos per page should we grab? Set low value
                        (10-50) for daily/weekly updates so there is less to
                        parse, set high value (200-500) for initial sync and
                        big updates so we hit flickr less.
  --force_update        If photo in db, override with new data.
  --photosets           Sync photosets (only photosets, no photos sync action
                        is run). Photos must be synced first. If photo from
                        photoset not in our db, it will be ommited.
  --collections         Sync collections. Photos and sets must be synced
                        first.
  --photos              Sync photos (only photos, no photosets sync action is
                        run).
  --update_photos       Update photos when updating a photoset.
  --update_tags         Update tags when updating a photo.
  -t, --test            Test/simulate. Don't write results to db.


Note: behavior soon to be changed (in 0.3.x releases) to simplify.

Download photos
----------------

::

./manage.py flickr_download [options]

::

  -u USER_ID, --user=USER_ID
                        Sync for a particular user. Default is 1 (in most
                        cases it's the admin and you're using it only for
                        yourself).
  -a, --all             By default downloads only photos which have not been
                        downloaded (default behavior). Use this option to
                        (re)download all.
  -p, --public          Only public photos.
  -l, --large           Large instead of original (f.ex. for accounts with no
                        access to original).
  -r, --reset           Clear downloads db table. Does not affect your files.

Photos are downloaded under your MEDIA folder. Default settings you can override:

.. code-block:: python

   # default settings
   FLICKR_DOWNLOAD_DIRBASE = 'flickr' # under MEDIA_ROOT
   FLICKR_DOWNLOAD_DIRFORMAT = '%Y/%Y-%m' # Photo.date_posted
   # photos with date_posted January 2009 will land in /media/flickr/2009/2009-01/

   # example custom settings
   FLICKR_DOWNLOAD_DIRBASE = 'downloads'
   FLICKR_DOWNLOAD_DIRFORMAT = '%Y/%m/%d'
   # photos with date_posted 23 January 2009 will land in /media/downloads/2009/01/23/ etc.

