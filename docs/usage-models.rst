.. _usage-models:

Models
======

.. code-block:: python

   from flickr.models import FlickrUser, Photo, PhotoSet, Collection

Basics
-------

Every model (except FlickrUser) is based on FlickrModel

.. code-block:: python

   class FlickrModel(models.Model):
       flickr_id = models.CharField(unique=True, db_index=True, max_length=50)
       user = models.ForeignKey(FlickrUser)
       show = models.BooleanField(default=True) #show the photo on your page?
       last_sync = models.DateTimeField(auto_now=True, auto_now_add=True)

       class Meta:
           abstract = True


Every object belongs to a FlickrUser which is mapped to a Django User

.. code-block:: python

   class FlickrUser(models.Model):
       user = models.OneToOneField(User)
       flickr_id = models.CharField(max_length=50, null=True, blank=True)
       nsid = models.CharField(max_length=32, null=True, blank=True)
       # ---- / more fields / -----
       token = models.CharField(max_length=128, null=True, blank=True) # authed
       perms = models.CharField(max_length=32, null=True, blank=True) # flickr permissions
       last_sync = models.DateTimeField(auto_now=True, auto_now_add=True)


Photo
-------

Selecting photos
~~~~~~~~~~~~~~~~~~~

.. code-block:: python
   
   # all photos
   Photo.objects.all()

   # only public photos
   Photo.objects.public()

   # only the ones with show=True
   #(default True, you can hide photos from viewing on your website by setting it False
   Photo.objects.visible()


Photo properties
~~~~~~~~~~~~~~~~~~~

Accessing properties of each photo is independent of the way you used to sync
them (check options in :ref:`usage-commands`), although some attributes may
not be available if you didn't sync your photos with the corresponding options.
The syntax is always the same:

.. code-block:: python

   (photo_object).(size_label).(property)

::

   size_label       - square: Square (75 x 75 pixels)
                    - largesquare: Large Square (150 x 150 pixels)
                    - thumb: Thumbnail (100 px on longest side)
                    - small: Small (240 px on longest side)
                    - small320: Small 320 (320 px on longest side)
                    - medium: Medium (500 px on longest side)
                    - medium640: Medium 640 (640 px on longest side)
                    - medium800: Medium 800 (800 px on longest side)
                    - large: Large (1024 px on longest side)
                    - large1600: Large 1600 (1600 px on longest side)
                    - large2048: Large 2048 (2048 px on longest side)
                    - ori: Original (original size)

   property         - source: url to image source.
                    - url: url to web page.
                    - width: width in pixels.
                    - height: height in pixels.


**Photo source** and **photo url web page** are either retrieved from the synced
data in the database (if ``--sizes`` option was used) or dynamically generated
(according to `Flickr docs <http://www.flickr.com/services/api/misc.urls.html>`_,
so this will always return a valid url for all **web sizes** (see `issue #20 <https://bitbucket.org/zalew/django-flickr/issue/20/photo-unavailable-hotlinks-for-certain>`_).

.. code-block:: python
   
   p = Photo.objects.get(id=123)
   p.large.source           # Image source url for large size.
   p.square.source          # source url for square image (75x75)...


**Special sizes** large 1600 and large 2048 are only available if used ``--sizes``
option while syncing and **original** will only be available for flickr pro accounts.

.. code-block:: python
   
   p.ori.url                # Url to web page for ori image.
   p.large2048.url          # Url to web page for ori image.


Photo **width** and **height** will only be available if ``flickr_sync`` was called
with the ``--sizes`` option.

.. code-block:: python
   
   p.ori.height             # Height of the original photo
   p.medium640.width        # Width for medium 640 size.



Some useful features
~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python
   
   p = Photo.objects.get(id=123)
   p.get_next() # next photo in order like on Flickr
   p.get_prev() # previous photo

   # link to the Flickr page. Works with every supported object: FlickrUser, Photo, Photoset, Collection.
   p.flickr_page_url


Photoset
----------


.. code-block:: python
   
   photoset = Photoset.objects.get(id=123)
   photo = Photo.objects.get(id=456)
   photo.get_next_in_photoset(photoset)
   photo.get_previous_in_photoset(photoset)
   photoset.cover() # returns the cover Photo


Collection
----------

.. code-block:: python
   
   c = Collection.objects.get(id=123)
   c.parent # if collection is nested
   c.sets.all() # sets in this collection
   c.icon # the collage picture you see on Flickr



