# coding=utf-8

from google.appengine.ext import db

from models_acc import *
from models import User
from georemindme.paging import *


class UserSettingsHelper(object):
    def get_by_id(self, id, async=False):
        key = db.Key.from_path(User.kind(), id, UserSettings.kind(), '%s_settings' % id)
        if async:
            return db.get_async(key)
        return db.get(key)
    
class UserProfileHelper(object):
    def get_by_id(self, id, async=False):
        key = db.Key.from_path(User.kind(), id, UserProfile.kind(), '%s_profile' % id)
        if async:
            return db.get_async(key)
        return db.get(key)

class UserCounterHelper(object):
    def get_by_id(self, id, async=False):
        key = db.Key.from_path(User.kind(), id, UserCounter.kind(), '%s_counters' % id)
        if async:
            return db.get_async(key)
        return db.get(key)
    
class UserTimelineHelper(object):
    def get_by_id(self, userid, page=1, query_id = None, vis='public'):
        '''
        Obtiene la lista de ultimos timeline del usuario

            :param userid: id del usuario (user.id)
            :type userid: :class:`string`
            :param page: numero de pagina a mostrar
            :type param: int
            :param query_id: identificador de busqueda
            :type query_id: int
            :returns: lista de tuplas de la forma [query_id, [(id, username, avatar)]]
        '''
        q = UserTimeline.all().filter('user =', db.Key.from_path(User.kind(), userid)).order('-created')
        p = PagedQuery(q, id = query_id, page_size=42)
        timelines = p.fetch_page(page)
        if vis.lower()=='public':
            return [p.id, [(timeline.id, timeline.created, timeline.user.username, timeline.instance.key() if timeline.instance is not None else None) for timeline in timelines if timeline._is_public()]]
        if vis.lower()=='shared':
            return [p.id, [(timeline.id, timeline.created, timeline.user.username, timeline.instance.key() if timeline.instance is not None else None) for timeline in timelines if timeline._is_shared() or timeline._is_public()]]
