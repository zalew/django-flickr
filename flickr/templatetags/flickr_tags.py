#!/usr/bin/env python
# encoding: utf-8
from django import template
register = template.Library()

@register.inclusion_tag("flickr/photo.html")
def flickr_photo(photo, size='medium', flickr_link=False):    
    return { 'photo' : photo, 'size': size, 'flickr_link': flickr_link, }