# coding=utf-8
from google.appengine.ext import db

from georemindme.paging import *
from models import User
from models_acc import UserFollowingIndex


class UserHelper(object):
    '''
        Do the queries needed to get a object
        Use ->  User.object.method()
    '''
    def get_by_key(self, key):
        return User.get(db.Key(encoded=key))
    
    def get_by_username(self, username, keys_only=False):
        if keys_only:
            return db.GqlQuery('SELECT __key__ FROM User WHERE username = :1', username).get()
        return User.gql('WHERE username = :1', username).get()
    
    def get_by_id(self, userid, keys_only=False):
        if keys_only:
            return db.Key.from_path(User.kind(), userid)
        return User.get_by_key_name(userid)
    
    def get_by_email(self, email):
        '''
         Search and returns a User object with that email
        '''
        if email is None:
            raise db.BadValueError("Wrong email")
            #user = self._get().filter('email =', email).filter('has =', 'confirmed:T').get()
        email = email.lower()
        user = self._get().filter('email =', email).get()
        return user
    
    def get_by_email_not_confirm(self, email):
        '''
         Search and returns a User object with that email
         Search users with confirm True or False
        '''
        if email is None:
            raise db.BadValueError("Wrong email")
        email = email.lower()
        user = self._get().filter('email =', email).filter('has =', 'confirmed:F').get()
        return user
    
    def get_followers(self, userid = None, username=None, page=1, query_id=None):
        '''
        Obtiene la lista de followers de un usuario
            
            :param userid: id del usuario (user.id)
            :type userid: :class:`string`
            :param username: nombre del usuario (user.username)
            :type username: :class:`string`
            :param page: numero de pagina a mostrar
            :type param: int
            :param query_id: identificador de busqueda
            :type query_id: int
            :returns: lista de tuplas de la forma [query_id, [(id, username, avatar)]]
        '''
        if username is not None:
            userkey = self.get_by_username(username, keys_only=True)
        elif userid is not None:
            userkey = db.Key.from_path(User.kind(), userid)
        followers = UserFollowingIndex.gql('WHERE following = :1', userkey)
        p = PagedQuery(followers, id = query_id)
        ##users = [(u.id, u.username, u.profile.avatar) for u in (index.parent() for index in p.fetch_page(page))]
        return [p.id, [(u.id, u.username, u.profile.avatar) for u in (index.parent() for index in p.fetch_page(page))]]
    
    def get_followings(self, userid = None, username=None, page=1, query_id=None):
        '''
        Obtiene la lista de personas a las que sigue el usuario
        
            :param userid: id del usuario (user.id)
            :type userid: :class:`string`
            :param username: nombre del usuario (user.username)
            :type username: :class:`string`
            :param page: numero de pagina a mostrar
            :type param: int
            :param query_id: identificador de busqueda
            :type query_id: int
            :returns: lista de tuplas de la forma [query_id, [(id, username, avatar)]]
        '''
        if username is not None:
            userkey = self.get_by_username(username, keys_only=True)
        elif userid is not None:
            userkey = db.Key.from_path(User.kind(), userid)
        followings = UserFollowingIndex.all().ancestor(userkey).order('-created')
        p = PagedQuery(followings, id = query_id)
        users = [db.get(index.following) for index in p.fetch_page(page)]  # devuelve una lista anidada con otra
        users = [(item.id, item.username, item.profile.avatar) for sublist in users for item in sublist]  # obtenemos las listas anidadas como una sola
        return [p.id, users]
    
    def _get(self, string=None):
        return User.all().filter('has =', 'active:T')