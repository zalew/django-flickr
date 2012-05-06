from xml.dom import minidom
import hashlib
import urllib
import urlparse
import json
from oauth2 import Consumer as OAuthConsumer, Token, Request as OAuthRequest, SignatureMethod_HMAC_SHA1
from urllib2 import HTTPError
import urllib2

class FlickrError(Exception): pass
class FlickrUnauthorizedCall(Exception): pass
class FlickrInvalidTokenAuth(Exception): pass

class BaseFlickrApi(object):
    """One of those APIs that don't do much. Simple Flickr auth and calling methods.
    
    Flickr's API docs: http://www.flickr.com/services/api/"""
    
    ENDPOINT = 'http://api.flickr.com/services/rest/'
    
    def __init__(self, key, secret, token=None, fallback=True):
        self.FLICKR_KEY = key
        self.FLICKR_SECRET = secret
        self.token = token
        self.fallback = fallback
        
    def _call_method(self, auth, **params):
        raise NotImplementedError
    
    def get(self, method, format='json', auth=True, **params):
        try:
            return self._call_method(auth=auth, method=method, format=format, **params)
        except FlickrInvalidTokenAuth, e:
            # Fall back to old flickr auth.
            from warnings import warn
            warn("FlickrAuthApi is deprecated, update to OAuthFlickrApi redirecting your users to '/auth/'")
            if self.fallback:
                old_api = FlickrAuthApi(self.FLICKR_KEY, self.FLICKR_SECRET, self.token)
                return old_api.get(method, format, auth, **params)
            else:
                raise FlickrError, 'No fall back to old Flickr Auth allowed.'



class OAuthFlickrApi(BaseFlickrApi):

    """Regular API call methods"""
        
    def get_consumer(self):
        return OAuthConsumer(self.FLICKR_KEY, self.FLICKR_SECRET)

    def get_token(self):
        try:
            return Token.from_string(self.token)
        except ValueError, e:
            if self.token:
                raise FlickrInvalidTokenAuth(e)
            else:
                raise FlickrError, 'Error when calling flickr API:  trying to build a token from an empty string'

    def get_oauth_request(self, url=None, token=None, **params):
        request = OAuthRequest.from_consumer_and_token(
                        self.get_consumer(),
                        token = token,
                        http_url = url or self.ENDPOINT,
                        parameters = params
                        )
        request.sign_request(SignatureMethod_HMAC_SHA1(), self.get_consumer(), token)
        return request
    
    def get_response(self, request):
        response = urllib2.urlopen(request.to_url())
        return '\n'.join(response.readlines())

    def _call_method(self, auth, **params):
        if params.get('format', 'json') == 'json': 
            params['nojsoncallback'] = 1
        if not params.get('method','').startswith('flickr.'):
            params['method'] = 'flickr.%s' % params['method']

        try:
            request = self.get_oauth_request(token = self.get_token() if auth else None, **params)
            data = self.get_response(request)
        except HTTPError, e:
            if e.code == 401:
                raise FlickrUnauthorizedCall, e
            else:
                raise
        except FlickrError:
            raise FlickrError, 'Error when calling flickr API:  %s' % e
        return json.loads(data)


    """ Auth methods """
    REQUEST_TOKEN_URL = 'http://www.flickr.com/services/oauth/request_token'
    AUTHORIZATION_URL = 'http://www.flickr.com/services/oauth/authorize'
    ACCESS_TOKEN_URL = 'http://www.flickr.com/services/oauth/access_token'

    def auth_url(self, request, perms='read', callback=None):
        """ Request token """
        params = {'oauth_callback': callback}
        rq = self.get_oauth_request(url=self.REQUEST_TOKEN_URL, token=None, **params)        
        response = self.get_response(rq)
        token = Token.from_string(response)
        request.session['flickr_token_session'] = token.to_string()
        
        """ User auth """
        params= {'perms' : perms,}
        rq = self.get_oauth_request(url=self.AUTHORIZATION_URL, token=token, **params)
        return rq.to_url()

    def access_token(self, request):
        oauth_token = request.session.get('flickr_token_session')
        if not oauth_token:
            raise FlickrError, 'No saved oauth_token from previous request, are sessions enabled?'
        token = Token.from_string(oauth_token)
        if token.key != request.GET.get('oauth_token', 'no-no-no'):
            raise FlickrError, 'oauth_token mismatch!'
        """ Access token """
        params = {'oauth_verifier' : request.GET.get('oauth_verifier') }
        rq = self.get_oauth_request(url=self.ACCESS_TOKEN_URL, token=token, **params)
        response = self.get_response(rq)
        self.token = Token.from_string(response).to_string()
        """ Check token """
        data = self.get('flickr.auth.oauth.checkToken')
        data['token'] = self.token
        return data


class FlickrAuthApi(BaseFlickrApi):
    """One of those APIs that don't do much. Simple Flickr auth and calling methods.
    
    Flickr's API docs: http://www.flickr.com/services/api/"""
    
    
    """Regular API call methods"""

    def __init__(self, key, secret, token=None):
        super(FlickrAuthApi, self).__init__(key, secret, token)
        from warnings import warn
        warn("FlickrAuthApi is deprecated, use OAuthFlickrApi instead")
    
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


""" OAuth by default """
FlickrApi = OAuthFlickrApi

    
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
