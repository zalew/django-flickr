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

.. code-block:: python
   :linenos:
  
   # all photos
   Photo.objects.all()
   
   # only public photos
   Photo.objects.public()
   
   # only the ones with show=True 
   #(default True, you can hide photos from viewing on your website by setting it False
   Photo.objects.visible()
   
   
Image properties

.. code-block:: python

   TODO
      
   
Some useful features

.. code-block:: python
   :linenos:

   p = Photo.objects.get(id=123)
   p.get_next() # next photo in order like on Flickr
   p.get_prev() # previous photo

   # link to the Flickr page. Works with every supported object: FlickrUser, Photo, Photoset, Collection.
   p.flickr_page_url 


Photoset
----------


.. code-block:: python
   :linenos:

   photoset = Photoset.objects.get(id=123)
   photo = Photo.objects.get(id=456)
   photo.get_next_in_photoset(photoset)
   photo.get_previous_in_photoset(photoset)
   photoset.cover() # returns the cover Photo


Collection
----------

.. code-block:: python
   :linenos:

   c = Collection.objects.get(id=123)
   c.parent # if collection is nested
   c.sets.all() # sets in this collection
   c.icon # the collage picture you see on Flickr



