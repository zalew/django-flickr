from bunch import bunchify
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render_to_response, get_object_or_404
from django.template.context import RequestContext
from django.utils import simplejson
from django.views.generic.list_detail import object_list
from flickr.api import FlickrApi, FlickrUnauthorizedCall
from flickr.models import FlickrUser, Photo, PhotoSet
from flickr.shortcuts import get_token_for_user


FLICKR_KEY = getattr(settings, 'FLICKR_KEY', None)
FLICKR_SECRET = getattr(settings, 'FLICKR_SECRET', None)
PERMS = getattr(settings, 'FLICKR_PERMS', None)


@login_required
def oauth(request):
    token = get_token_for_user(request.user)
    if not token:
        api = FlickrApi(FLICKR_KEY, FLICKR_SECRET)
        url = api.auth_url(request, perms=PERMS, callback= request.build_absolute_uri(reverse('flickr_complete')) )
        return HttpResponseRedirect(url)
    else:
        api = FlickrApi(FLICKR_KEY, FLICKR_SECRET, token, fallback=False)
        try:
            data = api.get('flickr.test.login')
        except:# FlickrUnauthorizedCall:
            fs = FlickrUser.objects.get(user=request.user)
            fs.token = None
            fs.perms = None
            fs.save()
            return HttpResponseRedirect(reverse('flickr_auth'))
    return render_to_response("flickr/auth_ok.html", { 'token': token }, context_instance=RequestContext(request))

@login_required
def oauth_access(request):
    api = FlickrApi(FLICKR_KEY, FLICKR_SECRET)
    data = api.access_token( request )
    if data:
        data = bunchify(data)
        fs, created = FlickrUser.objects.get_or_create(user=request.user)
        fs.token = data.token
        fs.nsid = data.oauth.user.nsid
        fs.username = data.oauth.user.username
        fs.full_name = data.oauth.user.fullname
        fs.perms = data.oauth.perms._content
        fs.save()
        return HttpResponseRedirect(reverse('flickr_auth'))
    raise Exception, 'Ups! No data...'
    

@login_required
def auth(request):
    from flickr.api import FlickrAuthApi
    api = FlickrAuthApi(FLICKR_KEY, FLICKR_SECRET)
    token = get_token_for_user(request.user)
    if not token:
        frob = request.GET.get('frob', None)
        if frob:        
            data = api.frob2token(frob)
            if data:            
                fs, created = FlickrUser.objects.get_or_create(user=request.user)
                token, perms = data.rsp.auth.token.text, data.rsp.auth.perms.text
                fs.token, fs.nsid, fs.username, fs.full_name, fs.perms = token, data.rsp.auth.user.nsid, data.rsp.auth.user.username, data.rsp.auth.user.fullname, perms
                fs.flickr_id = data.rsp.auth.user.nsid
                fs.save()
                return HttpResponseRedirect(reverse('flickr_auth_deprecated'))
        else:
            try:
                fs = FlickrUser.objects.get(user=request.user)
                token = fs.token
            except FlickrUser.DoesNotExist:
                auth_url = api.auth_url(PERMS) 
                return render_to_response("flickr/auth.html", { 'auth_url': auth_url }, context_instance=RequestContext(request))
    else:
        fs = FlickrUser.objects.get(user=request.user)
    return render_to_response("flickr/auth_ok.html", { 'token': fs.token }, context_instance=RequestContext(request))



def index(request, user_id=1):
    photos = Photo.objects.public()
    photosets = PhotoSet.objects.all()
    return object_list(request, 
        queryset = photos,
        paginate_by = 10, 
        extra_context = { 'photosets': photosets },
        template_object_name = 'photo',
        template_name = 'flickr/index.html'
        )


def photo(request, flickr_id):
    try:
        photo = Photo.objects.get(flickr_id=flickr_id)
    except Photo.DoesNotExist:
        photo = get_object_or_404(Photo, pk=flickr_id)
    return render_to_response("flickr/photo_page.html", { 'photo': photo }, context_instance=RequestContext(request))
        

def photoset(request, flickr_id):
    photoset = get_object_or_404(PhotoSet, flickr_id=flickr_id)
    photos = Photo.objects.public(photoset__id__in=[photoset.id,])
    photosets = PhotoSet.objects.all()
    return object_list(request, 
        queryset = photos,
        paginate_by = 10, 
        extra_context = { 'photoset': photoset, 'photosets': photosets },
        template_object_name = 'photo',
        template_name = 'flickr/index.html'
        )
       

def method_call(request, method):
    api = FlickrApi(FLICKR_KEY, FLICKR_SECRET)
    if request.user.is_authenticated():
        api.token = get_token_for_user(request.user)  
        auth = True
    else:
        auth = False    
    data = api.get(method, auth=auth, photo_id='6110054503')
    return HttpResponse(simplejson.dumps(data))
