from xml.dom import minidom
import hashlib
import urllib
import json


class FlickrError(Exception): pass


class FlickrApi(object):
    """One of those APIs that don't do much. Simple Flickr auth and calling methods.
    
    Flickr's API docs: http://www.flickr.com/services/api/"""
    
    ENDPOINT = 'http://api.flickr.com/services/rest/'
    
    def __init__(self, key, secret, token=None):
        self.FLICKR_KEY = key
        self.FLICKR_SECRET = secret
        self.token = token


    
    """Regular API call methods"""
   
    
    def _call_method(self, auth, **params):
        params['api_key'] = self.FLICKR_KEY
        params['auth_token'] = self.token
        if params.get('format', 'json') == 'json': 
            params['nojsoncallback'] = 1
        if not params.get('method','').startswith('flickr.'):
            params['method'] = 'flickr.%s' % params['method']                        
        url = '%s?%s'% (self.ENDPOINT, urllib.urlencode(sorted(params.items())))        
        if auth:
            if not self.token:
                raise FlickrError, 'You want to sign API call with token, but there is no token provided to FlickrApi.__init__(). \
                You can try calling your method with auth=False if you don\'t want to sign it.'
            url = '%s&api_sig=%s' % (url, hashlib.md5('%s%s' % (self.FLICKR_SECRET, ''.join(sorted(['%s%s' % (k,v) for k, v in params.iteritems()])))).hexdigest())
        try:
            f = urllib.urlopen(url)
        except Exception, e:
            raise FlickrError, 'Can\'t open url (%s), urllib.urlopen() failed with %s' % (url, e)
        return json.load(f)
    
    
    def get(self, method, format='json', auth=True, **params):
        return self._call_method(auth=auth, method=method, format=format, **params)
    
           
        
    """Auth methods"""
    
    
    def auth_url(self, perms='read'):
        auth_sig = hashlib.md5('%sapi_key%sperms%s' % (self.FLICKR_SECRET, self.FLICKR_KEY, perms)).hexdigest()
        return 'http://flickr.com/services/auth/?api_key=%s&perms=%s&api_sig=%s'% (self.FLICKR_KEY, perms, auth_sig)
    
        
    def _parse_xml(self, url):
        xml = minidom.parse(urllib.urlopen(url))
        data = unmarshal(xml)
        if not data.rsp.stat == 'ok':
            msg = "ERROR [%s]: %s" % (data.rsp.err.code, data.rsp.err.msg)
            raise FlickrError, msg
        return data
    
    
    def frob2token(self, frob):
        method = 'flickr.auth.getToken'
        auth_sig = hashlib.md5('%sapi_key%sfrob%smethod%s' % (self.FLICKR_SECRET, self.FLICKR_KEY, frob, method)).hexdigest()
        url = '%s?api_key=%s&method=%s&api_sig=%s&frob=%s' % (self.ENDPOINT, self.FLICKR_KEY, method, auth_sig, frob)
        data = self._parse_xml(url)
        return data
    
    
    
    
    
   
    
"""
below is taken from
    flickr.py
    Copyright 2004-2006 James Clarke <james@jamesclarke.info>
    Portions Copyright 2007-2008 Joshua Henderson <joshhendo@gmail.com>
    http://code.google.com/p/flickrpy/
"""
class Bag: pass
#unmarshal taken and modified from pyamazon.py
#makes the xml easy to work with
def unmarshal(element):
    rc = Bag()
    if isinstance(element, minidom.Element):
        for key in element.attributes.keys():
            setattr(rc, key, element.attributes[key].value)
            
    childElements = [e for e in element.childNodes \
                     if isinstance(e, minidom.Element)]
    if childElements:
        for child in childElements:
            key = child.tagName
            if hasattr(rc, key):
                if type(getattr(rc, key)) <> type([]):
                    setattr(rc, key, [getattr(rc, key)])
                setattr(rc, key, getattr(rc, key) + [unmarshal(child)])
            elif isinstance(child, minidom.Element) and \
                     (child.tagName == 'Details'):
                # make the first Details element a key
                setattr(rc,key,[unmarshal(child)])
                #dbg: because otherwise 'hasattr' only tests
                #dbg: on the second occurence: if there's a
                #dbg: single return to a query, it's not a
                #dbg: list. This module should always
                #dbg: return a list of Details objects.
            else:
                setattr(rc, key, unmarshal(child))
    else:
        #jec: we'll have the main part of the element stored in .text
        #jec: will break if tag <text> is also present
        text = "".join([e.data for e in element.childNodes \
                        if isinstance(e, minidom.Text)])
        setattr(rc, 'text', text)
    return rc