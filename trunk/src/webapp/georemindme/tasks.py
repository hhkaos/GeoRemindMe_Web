# coding=utf-8

import os
from django.http import HttpResponse, HttpResponseForbidden, HttpResponseBadRequest
from django.views.decorators.csrf import csrf_exempt

from google.appengine.api.taskqueue import *
from google.appengine.ext import db
from google.appengine.api import mail




def admin_required(func):
    def _wrapper(*args, **kwargs):
        if 'HTTP_X_APPENGINE_TASKNAME' in os.environ:
            return func(*args, **kwargs)
        session = args[0].session
        user = session.get('user')
        if user and user.is_admin():
            return func(*args, **kwargs)
        return HttpResponseForbidden()
    return _wrapper


class TaskHandler(object):
    def add(self):
        pass
    
#===============================================================================
# ENVIO DE EMAILS
#===============================================================================
class EmailHandler(TaskHandler):
    '''
    Clase encargada de gestionar la cola de envio de correos
    '''
    def add(self, email):
        task = Task(url='/tasks/email/', params = { 'sender': email.sender,
                                                   'to': email.to,
                                                   'subject': email.subject,
                                                   'html': email.html
                                                   },
                                        method = 'POST')
        task.add(queue_name='email')


@csrf_exempt
@admin_required
def email_worker(request):
    mail.send_mail(request.POST['sender'], request.POST['to'], request.POST['subject'], request.POST['html'])
    return HttpResponse()

#===============================================================================
# NOTIFICACIONES A FOLLOWERS
#===============================================================================
class NotificationHandler(TaskHandler):
    def timeline_followers_notify(self, timeline):
        task = Task(url='/tasks/notify/timeline/', params = { 'timeline': timeline.key() }, method = 'POST')
        task.add(queue_name='timelineFollowers')
        
    def list_followers_notify(self, list):
        '''
        Notifica a los seguidores de la lista que esta se modifico
        '''
        task = Task(url='/tasks/notify/list', params = {'list': list.key()}, method = 'POST')
        task.add(queue_name='listFollowers')
    
@csrf_exempt
@admin_required
def timelinefollowers_worker(request):
    timeline = db.get(request.POST['timeline'])
    notified = timeline.notify_followers()
    if notified:
        return HttpResponse()
    return HttpResponseBadRequest()

@csrf_exempt
@admin_required
def list_notify_worker(request):
    list = db.get(request.POST['list'])
    notified = list.notify_followers()
    if notified:
        return HttpResponse()
    return HttpResponseBadRequest()
    
        
        
    