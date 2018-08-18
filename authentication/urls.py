import os

from django.urls import re_path

from rest_framework.routers import DefaultRouter

from . views import AccountRegistration, AccountLogin, AccountViewSet


accounts = DefaultRouter()
accounts.register(r'accounts', AccountViewSet)

cwd = os.path.abspath(os.path.dirname(__file__)).split('/')[-1]
app_name = cwd  # current working directory
urlpatterns = [
    re_path(r'register/$', AccountRegistration.as_view()),
    re_path(r'login/$', AccountLogin.as_view()),
]

urlpatterns += accounts.urls
