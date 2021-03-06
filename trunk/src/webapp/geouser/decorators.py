# coding=utf-8

from django.http import HttpResponseRedirect


"""
   login_required decorator
   It is used to check if a user is logged in or not
"""
def login_required(func):
    def _wrapper(*args, **kwargs):
        session = args[0].session  # request es el primer parametro que pasamos
        user = session.get('user')
        if user and user.is_authenticated():
            return func(*args, **kwargs)
        from views import login
        return login(args[0])
    return _wrapper
