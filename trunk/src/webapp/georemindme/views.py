# coding=utf-8

from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.utils.translation import ugettext as _

from stats import *
from tasks import *

def home(request, login=False):
    if request.session.get('user'):
        return HttpResponseRedirect(reverse('geouser.views.dashboard'))
    
    return render_to_response("webapp/home.html", {'login' :login}, context_instance=RequestContext(request))

def private_home(request,login=False):
    if request.session.get('user'):
        return HttpResponseRedirect(reverse('geouser.views.dashboard'))
    return render_to_response("webapp/home_private_beta.html", {'login' :login}, context_instance=RequestContext(request))

def set_language(request):
    if request.method == 'POST':
        from django.conf import settings
        available = dict(settings.LANGUAGES)
        lang = request.POST.get('lang', settings.LANGUAGE_CODE)
        next = request.POST.get('next', '/')
        if lang in available: #we have the lang_code
            request.session['LANGUAGE_CODE'] = lang
        if request.session.get('user', None):
            settings = request.session['user'].settings
            settings.language = lang
            settings.put()
        return HttpResponseRedirect(next)
        
    return HttpResponseRedirect(request.path)

