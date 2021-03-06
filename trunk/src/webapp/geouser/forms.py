# coding=utf-8

from django import forms
from django.utils.translation import ugettext as _
from django.conf import settings
from google.appengine.ext.db import GeoPt, NotSavedError

from models import User


class EmailForm(forms.Form):
    email = forms.EmailField(required=True)


class RecoverPassForm(forms.Form):
    password = forms.CharField(required=True, max_length=settings.MAX_PWD_LENGTH,
                               min_length=settings.MIN_PWD_LENGTH,
                               widget=forms.PasswordInput(attrs={'size': settings.MAX_PWD_LENGTH+2})
                               )
    password2 = forms.CharField(label=_("Repeat password"), required=True,
                               max_length=settings.MAX_PWD_LENGTH,
                               min_length=settings.MIN_PWD_LENGTH,
                               widget=forms.PasswordInput(attrs={'size': settings.MAX_PWD_LENGTH+2})
                               )

    def clean(self):
        """
         Clean data and check if the two passwords are the same
        """
        cleaned_data = self.cleaned_data
        password = cleaned_data.get('password')
        password2 = cleaned_data.get('password2')

        if password and password2:
            if password.find(' ') != -1:
                msg = _("Passwords can't have white spaces")
                self._errors['password'] = self.error_class([msg])

            if password != password2:
                msg = _("Passwords must be the same.")
                self._errors['password'] = self.error_class([msg])

        return cleaned_data


class LoginForm(forms.Form):
    """
        Form for the login process
    """
    email = forms.EmailField(required=True)
    password = forms.CharField(required=True, max_length=settings.MAX_PWD_LENGTH,
                               widget=forms.PasswordInput(attrs={'size': settings.MAX_PWD_LENGTH+2})
                               )
    remember_me = forms.BooleanField(label=_("Remember me?"), required=False,
                                     widget=forms.CheckboxInput()
                                     )


class RegisterForm(forms.Form):
    """
        Form for the register process
    """
    email = forms.EmailField(required=True)
    password = forms.CharField(required=True, max_length=settings.MAX_PWD_LENGTH,
                               min_length=settings.MIN_PWD_LENGTH,
                               widget=forms.PasswordInput(attrs={'size': settings.MAX_PWD_LENGTH+2})
                               )
    password2 = forms.CharField(label=_("Repeat password"), required=True,
                               max_length=settings.MAX_PWD_LENGTH,
                               min_length=settings.MIN_PWD_LENGTH,
                               widget=forms.PasswordInput(attrs={'size': settings.MAX_PWD_LENGTH+2})
                               )

    def clean(self):
        """
         Clean data and check if the two passwords are the same
        """
        cleaned_data = self.cleaned_data
        password = cleaned_data.get('password')
        password2 = cleaned_data.get('password2')

        if password and password2:
            if password.find(' ') != -1:
                msg = _("Passwords can't have white spaces")
                self._errors['password'] = self.error_class([msg])

            if password != password2:
                msg = _("Passwords must be the same.")
                self._errors['password'] = self.error_class([msg])

        return cleaned_data

    def save(self, language='en', commit=True):
        try:
            return User.register(email=self.cleaned_data['email'], password=self.cleaned_data['password'], language=language)
        except User.UniqueEmailConstraint, e:
            fail = _('Email already in use')
            self._errors['email'] = self.error_class([fail])
        except Exception, e:  # new user is not in DB so raise NotSavedError instead of UniqueEmailConstraint
            fail = _(e.message)
            self._errors['email'] = self.error_class([fail])
            
class SocialUserForm(forms.Form):
    '''
        Formulario para pedir un correo y username a los usuarios que entran desde una red social
    '''
    email = forms.EmailField(label=_('email'), required=True)
    username = forms.CharField(label=_('username'), required=True)
    '''
    password = forms.CharField(label=_("New password"), required=False,
                               max_length=settings.MAX_PWD_LENGTH,
                               min_length=settings.MIN_PWD_LENGTH,
                               widget=forms.PasswordInput(attrs={'size': settings.MAX_PWD_LENGTH+2})
                               )
    password2 = forms.CharField(label=_("Repeat new password"), required=False,
                               max_length=settings.MAX_PWD_LENGTH,
                               min_length=settings.MIN_PWD_LENGTH,
                               widget=forms.PasswordInput(attrs={'size': settings.MAX_PWD_LENGTH+2})
                               )
    
    def clean(self):
        """
         Clean data and check if the old pass is input and the two passwords are the same
        """
        cleaned_data = self.cleaned_data
        password = cleaned_data.get('password')
        password2 = cleaned_data.get('password2')

        if password.find(' ') != -1:
            msg = _("Passwords can't have white spaces")
            self._errors['password'] = self.error_class([msg])
        elif password != password2:
            msg = _("Passwords must be the same.")
            self._errors['password'] = self.error_class([msg])
        return cleaned_data
    '''
    def save(self, user):
        try:
            return user.update(email=self.cleaned_data['email'], username=self.cleaned_data['username'])
        except User.UniqueEmailConstraint, e:
            fail = _('Email already in use')
            self._errors['email'] = self.error_class([fail])
        except User.UniqueUsernameConstraint, e:
            fail = _('Username already in use')
            self._errors['username'] = self.error_class([fail])
        except Exception, e:  # new user is not in DB so raise NotSavedError instead of UniqueEmailConstraint
            fail = _(e.message)
            self._errors['email'] = self.error_class([fail])


class UserProfileForm(forms.Form):
    username = forms.CharField(label=_('Username'), required=True)
    
    def save(self, user, file=None):
        if file is not None:
            if 'image/' in file.type:
                user.profile.avatar = file
        try:
            user.update(username=self.cleaned_data['username'])
            return True
        except User.UniqueUsernameConstraint, e:
            fail = _('Username already in use')
            self._errors['username'] = self.error_class([fail])
        except Exception, e:  # new user is not in DB so raise NotSavedError instead of UniqueEmailConstraint
            fail = _(e.message)
            self._errors['email'] = self.error_class([fail])
        


class UserForm(forms.Form):
    """
        Allow the user to change somo info of his account
    """
    email = forms.EmailField(required=True)
    old_pass = forms.CharField(label=_("Current password"), required=False,
                               max_length=settings.MAX_PWD_LENGTH,
                               min_length=settings.MIN_PWD_LENGTH,
                               widget=forms.PasswordInput(attrs={'size': settings.MAX_PWD_LENGTH+2})
                               )
    password = forms.CharField(label=_("New password"), required=False,
                               max_length=settings.MAX_PWD_LENGTH,
                               min_length=settings.MIN_PWD_LENGTH,
                               widget=forms.PasswordInput(attrs={'size': settings.MAX_PWD_LENGTH+2})
                               )
    password2 = forms.CharField(label=_("Repeat new password"), required=False,
                               max_length=settings.MAX_PWD_LENGTH,
                               min_length=settings.MIN_PWD_LENGTH,
                               widget=forms.PasswordInput(attrs={'size': settings.MAX_PWD_LENGTH+2})
                               )

    def clean(self):
        """
         Clean data and check if the old pass is input and the two passwords are the same
        """
        cleaned_data = self.cleaned_data
        old_pass = cleaned_data.get('old_pass')
        password = cleaned_data.get('password')
        password2 = cleaned_data.get('password2')

        if password or password2:
            if old_pass:  # to change password, user must write old pass first
                if password.find(' ') != -1:
                    msg = _("Passwords can't have white spaces")
                    self._errors['password'] = self.error_class([msg])
                elif password != password2:
                    msg = _("Passwords must be the same.")
                    self._errors['password'] = self.error_class([msg])
            else:
                msg = _("Old password needed.")
                self._errors['old_pass'] = self.error_class([msg])
        return cleaned_data

    def save(self, user, commit=True):
        email = self.cleaned_data['email']
        old_pass = self.cleaned_data['old_pass']
        password = self.cleaned_data['password']

        if old_pass != "" and password != "":  # user wants to change password
            if user.check_password(old_pass):
                user.password = password
            else:
                msg = _("Old password wrong.")
                self._errors['old_pass'] = self.error_class([msg])
                return None
        elif email != user.email:  # user only wants to change the email
            user.email = email

        if commit:
            try:
                user.put()
            except User.UniqueEmailConstraint:  # email already in use
                msg = _("email already in use")
                self._errors['email'] = self.error_class([msg])
                return None
            except Exception:
                msg = _("A error ocurred, try again later")
                self._errors['email'] = self.error_class([msg])
                return None

        return user
