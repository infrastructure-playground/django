from __future__ import unicode_literals

from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
# from django.core.urlresolvers import reverse
from django.db import models


class AccountManager(BaseUserManager):
    def create_user(self, password=None, **kwargs):
        print('===Password===')
        print(password)
        print('===Kwargs====')
        print(kwargs)
        if not kwargs.get('email'):
            raise ValueError('Users must have a valid email address.')

        if not kwargs.get('username'):
            raise ValueError('Users must have a valid username.')

        if password == kwargs.get('confirm_password'):
            del kwargs['confirm_password']
        else:
            raise ValueError('Passwords must match')

        account = self.model(**kwargs)

        account.set_password(password)
        account.save()

        return account

    def create_superuser(self, password, **kwargs):
        kwargs['confirm_password'] = password
        account = self.create_user(password, **kwargs)

        account.is_admin = True
        account.save()

        return account


class Account(AbstractBaseUser):
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=40, unique=True)

    first_name = models.CharField(max_length=40)
    middle_name = models.CharField(max_length=40, null=True, blank=True)
    last_name = models.CharField(max_length=40)

    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = AccountManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __unicode__(self):
        return self.email

    def get_full_name(self):
        return ' '.join([self.first_name, self.last_name])

    def get_short_name(self):
        return self.first_name

    # def get_absolute_url(self):
        # user_id came from the URL parameter in the urls.py
        # return reverse('users-detail', kwargs={'user_id': self.id})
