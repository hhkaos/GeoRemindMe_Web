# coding=utf-8

import logging

from signals import *
from exceptions import *

from geouser.models_acc import UserTimelineSystem
from models_poi import *


def new_alert(sender, **kwargs):
    '''
    Se registra una nueva alerta
    '''
    if isinstance(sender, Alert):
        timeline = UserTimelineSystem(user = sender.user, instance = sender, msg_id=200)
    elif isinstance(sender, AlertSuggestion):
        timeline = UserTimelineSystem(user = sender.user, instance = sender, msg_id=320)
    else:
        return
    timeline.put()
alert_new.connect(new_alert)

def modified_alert(sender, **kwargs):
    '''
    Se modifica una alerta
    '''
    if isinstance(sender, Alert):
        timeline = UserTimelineSystem(user = sender.user, instance = sender, msg_id=201)
    elif isinstance(sender, AlertSuggestion):
        timeline = UserTimelineSystem(user = sender.user, instance = sender, msg_id=321)
    else:
        return
    timeline.put()
alert_modified.connect(modified_alert)

def deleted_alert(sender, **kwargs):
    '''
    Se borra una alerta
    '''
    if isinstance(sender, Alert):
        timeline = UserTimelineSystem(user = sender.user, instancem = sender, msg_id=202)
    elif isinstance(sender, AlertSuggestion):
        timeline = UserTimelineSystem(user = sender.user, instance = sender, msg_id=322)
    else:
        return
    timeline.put()
alert_deleted.connect(deleted_alert)

def done_alert(sender, **kwargs):
    if isinstance(sender, Alert):
        timeline = UserTimelineSystem(user = sender.user, instance = sender, msg_id=203)
    elif isinstance(sender, AlertSuggestion):
        timeline = UserTimelineSystem(user = sender.user, instance = sender, msg_id=323)
    else:
        return
    timeline.put()
alert_done.connect(done_alert)

def new_suggestion(sender, **kwargs):
    timeline = UserTimelineSystem(user = sender.user, instance = sender, msg_id=300)
    timeline.put()
suggestion_new.connect(new_suggestion)

def modified_suggestion(sender, **kwargs):
    timeline = UserTimelineSystem(user = sender.user, instance = sender, msg_id=301)
    timeline.put()
suggestion_modified.connect(new_suggestion)

def deleted_suggestion(sender, **kwargs):
    timeline = UserTimelineSystem(user = sender.user, instance = sender, msg_id=302)
    timeline.put()
suggestion_deleted.connect(deleted_suggestion)

def new_following_suggestion(sender, **kwargs):
    timeline = UserTimelineSystem(user = kwargs['user'], instance = sender, msg_id=333)
    timeline.put()
suggestion_following_new.connect(new_following_suggestion)

def deleted_following_suggestion(sender, **kwargs):
    timeline = UserTimelineSystem(user = kwargs['user'], instance = sender, msg_id=304)
    timeline.put()
suggestion_following_deleted.connect(deleted_following_suggestion)

def new_place(sender, **kwargs):
    if isinstance(sender, PrivatePlace):
        timeline = UserTimelineSystem(user = sender.user, instance = sender, msg_id=400)
    elif isinstance(sender, Place):
        timeline = UserTimelineSystem(user = sender.user, instance = sender, msg_id=450)
    else:
        return
    timeline.put()
place_new.connect(new_place)

def modified_place(sender, **kwargs):
    if isinstance(sender, PrivatePlace):
        timeline = UserTimelineSystem(user = sender.user, instance = sender, msg_id=401)
    elif isinstance(sender, Place):
        timeline = UserTimelineSystem(user = sender.user, instance = sender, msg_id=451)
    else:
        return
    timeline.put()
place_modified.connect(modified_place)

def deleted_place(sender, **kwargs):
    if isinstance(sender, PrivatePlace):
        timeline = UserTimelineSystem(user = sender.user, instance = sender, msg_id=402)
    elif isinstance(sender, Place):
        timeline = UserTimelineSystem(user = sender.user, instance = sender, msg_id=452)
    else:
        return
    timeline.put()
place_deleted.connect(deleted_place)

from models import *