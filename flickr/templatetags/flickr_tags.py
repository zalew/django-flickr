#!/usr/bin/env python
# encoding: utf-8
from django import template
import datetime
register = template.Library()


@register.inclusion_tag("flickr/photo.html")
def flickr_photo(photo, size='medium', flickr_link=False):
    if not photo:
        return {}
    if size == 'large' and photo.date_posted <= datetime.datetime(2010, 05, 25):
        if photo.user.ispro:
            size = 'ori'
        else:
            size = 'medium640'
    return {'photo': photo, 'size': size, 'flickr_link': flickr_link, 'photo_size': getattr(photo, size)}
