from cgi import parse_qs
import oauth2

from django.http import HttpResponse, HttpResponseBadRequest,HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.utils.translation import ugettext as _
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from django.core.urlresolvers import reverse
from django.contrib import messages

from geouser.forms import LoginForm
from geouser.decorators import login_required
from geouser.funcs import login_func, init_user_session
from server import OAUTH_Server
from models import OAUTH_Access

@csrf_exempt
def token_request(request):
    try:
        server = OAUTH_Server()
        oauthToken = server.token_requested(request)
    except Exception, e:
        return HttpResponseBadRequest(e)
    return HttpResponse(oauthToken)

def authorize_token_request(request):
    if not 'oauth_token' in request.GET:
        return HttpResponseBadRequest()
    else:
        if 'user' in request.session and request.session['user'].is_authenticated():
            server = OAUTH_Server()
            if request.method == 'POST':
                if 'accept' in request.POST:#el token ha sido aceptado
                    token = server.authorization_token_requested(request, request.session['user'])
                    if token.callback is not None:#devolvemos al usuario al callback
                        return HttpResponseRedirect('%s?oauth_token=%s&oauth_verifier=%s' % (token.callback, token.key, token.verifier))
                    else:#no hay callback
                        # TODO: mirar si es una aplicacion por PIN
                        return HttpResponse('oauth_token=%s&oauth_verifier=%s' % (token.key, token.verifier))
                else:
                    return HttpResponseRedirect('/')
            else:
                appInfo = server.appInfo_requested(request.GET['oauth_token'])
                return render_to_response('oauth/authorization.html', {'appInfo' : appInfo}, context_instance=RequestContext(request))
        else:
            #el usuario necesita identificarse primero
            if request.method == 'POST':
                f = LoginForm(request.POST, prefix='user_login')
                
                if f.is_valid():
                    error, redirect = login_func(request, f.cleaned_data['email'], f.cleaned_data['password'], f.cleaned_data['remember_me'])
                    if error == '':#el usuario se ha identificado, recargamos la pagina
                        return HttpResponseRedirect(request.get_full_path())
                else:
                    error = _("The email/password you entered is incorrect<br/>Please make sure your caps lock is off and try again")
            else:
                error = ''
                f = LoginForm(prefix='user_login')
            return render_to_response('oauth/login.html', {'error': error, 'form':f}, context_instance=RequestContext(request))

@csrf_exempt
def access_token_request(request):
    try:
        server = OAUTH_Server()
        oauthToken = server.access_token_requested(request)
    except Exception, e:
        return HttpResponseBadRequest(e)
    return HttpResponse(oauthToken)

#------------------------------------------------------------------------------ 
# CLIENTE
#------------------------------------------------------------------------------ 

@login_required
def client_token_request(request, provider):
    OAUTH = settings.OAUTH
    provider = provider.lower()
    consumer = oauth2.Consumer(OAUTH[provider]['app_key'], OAUTH[provider]['app_secret'])
    client = oauth2.Client(consumer) 
    response, content = client.request(OAUTH[provider]['request_token_url'], "GET", callback=OAUTH[provider]['callback_url'])
    if response['status'] != '200':
        raise Exception("Invalid response from server.")

    params = parse_qs(content, keep_blank_values=False)
    
    request.session[provider] = {'request_token' : {
                                                    'oauth_token_secret' : params['oauth_token_secret'][0], 
                                                    'oauth_token' : params['oauth_token'][0],
                                                    'oauth_callback_confirmed' : params['oauth_callback_confirmed'][0]
                                                    }
                                 }
    url = "%s?oauth_token=%s&oauth_callback=%s" % (OAUTH[provider]['authorization_url'],
        request.session[provider]['request_token']['oauth_token'], OAUTH[provider]['callback_url'])
    
    return HttpResponseRedirect(url)

@csrf_exempt
def client_access_request(request, provider):
    provider = provider.lower()
    if not request.session[provider]['request_token']['oauth_token'] == request.GET.get('oauth_token') \
            and request.GET.get('oauth_verifier') :
        messages.error(request, _("Invalid response from server."))
        return HttpResponseRedirect(reverse('georemindme.views.home'))
    #lee el token recibido
    token = oauth2.Token(request.GET.get('oauth_token'), 
                         request.session[provider]['request_token']['oauth_token_secret'])
    token.set_verifier(request.GET.get('oauth_verifier'))
    
    consumer = oauth2.Consumer(settings.OAUTH[provider]['app_key'],
                               settings.OAUTH[provider]['app_secret'])
    client = oauth2.Client(consumer, token) 
    #lo intercambia por un token de acceso
    response, content = client.request(settings.OAUTH[provider]['access_token_url'], "GET")
    if response['status'] != '200':
        raise Exception("Invalid response from server.")
    params = parse_qs(content, keep_blank_values=False)
    token = {   
                'oauth_token_secret' : params['oauth_token_secret'][0], 
                'oauth_token' : params['oauth_token'][0],
            }
    if provider == 'twitter':
        from clients import TwitterClient
        client = TwitterClient(token=oauth2.Token(token['oauth_token'], token['oauth_token_secret']))
        if 'user' in request.session:#usuario ya esta logeado, guardamos el token de su cuenta
            if client.authorize(request.session['user']):
                messages.success(request, _('Got access from %s' % provider))
        else:
            user = client.authenticate()
            messages.success(request, _('Logged from %s' % provider))
            init_user_session(request, user)
    else:
        raise Exception("Invalid server.")
    return HttpResponseRedirect(reverse('geouser.views.dashboard'))
    
#===============================================================================
# LOGIN WITH OAUTH
#===============================================================================
def authenticate_request(request, provider):
    #normalmente la diferencia con client_token_request es que peticion se hace a la url /authenticate en vez de /authorize
    OAUTH = settings.OAUTH
    provider = provider.lower()
    consumer = oauth2.Consumer(OAUTH[provider]['app_key'], OAUTH[provider]['app_secret'])
    client = oauth2.Client(consumer) 
    response, content = client.request(OAUTH[provider]['request_token_url'], "GET", callback=OAUTH[provider]['callback_url'])
    if response['status'] != '200':
        raise Exception("Invalid response from server.")
    params = parse_qs(content, keep_blank_values=False)
    request.session[provider] = {'request_token' : {
                                                    'oauth_token_secret' : params['oauth_token_secret'][0], 
                                                    'oauth_token' : params['oauth_token'][0],
                                                    'oauth_callback_confirmed' : params['oauth_callback_confirmed'][0]
                                                    }
                                 }
    url = "%s?oauth_token=%s&oauth_callback=%s" % (OAUTH[provider]['authenticate_url'],
        request.session[provider]['request_token']['oauth_token'], OAUTH[provider]['callback_url'])

    return HttpResponseRedirect(url)