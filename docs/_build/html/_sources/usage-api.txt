.. _usage-api:

Flickr API
=========

Using the API is easy. Here's an example authorized call to `flickr.people.getPhotos
<https://secure.flickr.com/services/api/explore/flickr.people.getPhotos>`_. 

.. code-block:: python
   :linenos:

   
   from flickr.api import FlickrApi   
   
   FLICKR_KEY = getattr(settings, 'FLICKR_KEY', None)
   FLICKR_SECRET = getattr(settings, 'FLICKR_SECRET', None)
   PERMS = getattr(settings, 'FLICKR_PERMS', None)
   
   api = FlickrApi(FLICKR_KEY, FLICKR_SECRET)
   api.get('flickr.people.getPhotos') 

   # Returns JSON by default. If you want XML:
   api.get('people.getPhotos', format='xml') # yep, also works without 'flickr.'

Currently supports only read methods with GET. Writing with POST soon to be implemented.