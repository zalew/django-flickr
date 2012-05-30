.. _install:

Installation
============


Using PIP
---------

The latest stable-ish build::

    pip install django-flickr

Development version::

    pip install hg+https://bitbucket.org/zalew/django-flickr



From source
-----------

::

    hg clone https://bitbucket.org/zalew/django-flickr
    cd django-flickr
    ./setup.py install



Dependencies
------------

* `Django`_ 1.4
* `Bunch`_ - to ease up managing json data
* `Taggit`_ - for handling tags
* `Taggit-templatetags`_ - not obligatory really, but it's an awesome addition to taggit and the example view uses it
* `Oauth2`_ - for auth

.. _`Django`: https://www.djangoproject.com/
.. _`Bunch`: http://pypi.python.org/pypi/bunch
.. _`Taggit`: https://github.com/alex/django-taggit
.. _`Taggit-templatetags`: https://github.com/feuervogel/django-taggit-templatetags
.. _`Oauth2`: http://pypi.python.org/pypi/oauth2



Configuration
-------------

Add 'flickr' to your INSTALLED_APPS and syncdb

Go to 'Your apps' on Flickr and generate an API key for your app. Put those data in your settings.py::

    FLICKR_KEY = 'xxxxxxxxxxxx'
    FLICKR_SECRET = 'xxxxxxx'
    FLICKR_PERMS = 'read'

and add flickr.urls to your urls.py



Authenticate your Flickr account
---------------------------------

Run your django app, sign in. Go to /flickr/auth/ and click on the link. Authorize your app on flickr. If your app is public, you'll be redirected to complete the auth process, if not (f.ex. you set up some bogus link), just copy the GET frob variables to your /flickr/auth url. Currently it uses FlickrAuth (set to be deprecated some day probably), not Oauth. (Oauth support is implemented, but untested well. You can try it.)

http://blog.flickr.net/en/2012/01/13/start-the-new-year-fresh/

  The Flickr API fully supports oAuth, which is already used by hundreds of Flickr apps, but there are still some apps that use the old authentication system, called FlickrAuth. We are asking all developers to move over to the new standard bu July 31. There is a related blog post on this topic on our engineering blog code.flickr.com.


Upgrading
----------

`South
<http://south.readthedocs.org/en/latest/index.html>`_ is used for migrations. Project is in early stages so expect them.





