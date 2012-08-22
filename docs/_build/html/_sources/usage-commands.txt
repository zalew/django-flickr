.. _usage-commands:

Management Commands
===================


Sync photos database
---------------------

::

./manage.py flickr_sync [options]

::

  -u USER_ID, --user=USER_ID
                        Sync for a particular user. Default is 1 (in most
                        cases it's the admin and you're using it only for
                        yourself).
  -i, --info            Fetch info for photos. It will take a long time to
                        sync as it needs to fetch Flickr data for every photo
                        separately.
  -e, --exif            Fetch exif for photos. It will take a long time to
                        sync as it needs to fetch Flickr data for every photo
                        separately.
  -s, --sizes           Fetch sizes details for photos. It is not needed,
                        sizes can be obtained dynanmically. It will take a
                        long time as it needs to fetch Flickr data for every
                        photo separately.
  -g, --geo             Fetch geo data for photos. It will take a long time as
                        it needs to fetch Flickr data for every photo
                        separately.
  -p, --photosets       Sync photosets. Photos must be synced first. If photo
                        from photoset not in our db, it will be ommited.
  -c, --collections     Sync collections. Photos and sets must be synced
                        first.
  --no-photos           Don't sync photos.
  --update-photos       Update outdated photos. It will take a long time as
                        it needs to call Flickr api several times per photo.
  --update-photos       Update tags in photos.
  -d DAYS, --days=DAYS  Sync photos from the last n days.
  --page=PAGE           Grab a specific portion of photos. To be used with
                        --per_page.
  --per-page=PER_PAGE   How many photos per page should we grab? Set low value
                        (10-50) for daily/weekly updates so there is less to
                        parse, set high value (200-500) for initial sync and
                        big updates so we hit flickr less.
  --ils                 Ignore last_sync.
  --initial             It assumpts db flickr tables are empty and blindly
                        hits create().
  -t, --test            Test/simulate. Don't write results to db.




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
  -s, --size            Specify size for download (by default original for pro
                        accounts and large for non-pro).
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

