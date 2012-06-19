.. _usage-intro:

Introduction
===================
  

How it works
-------------


* Flickr API is hit only for syncing via management commands. 
* You can choose if you want to sync only crucial photo information (1 API call per page of X photos) or fetch additional information (increases the number of API calls and execution time).
* The application works with data downloaded from Flickr and saved to the project's database. No API call is made when selecting and viewing data.
* Displayed photos are hotlinked from Flickr, but you can download the original photos and access/process them locally if you wish. 