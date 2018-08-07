from django.urls import re_path

from rest_framework.routers import DefaultRouter

from . views import AccountRegistration, AccountLogin, AccountViewSet


accounts = DefaultRouter()
accounts.register(r'', AccountViewSet)

app_name = 'authentication'
urlpatterns = [
    re_path(r'register/$', AccountRegistration.as_view()),
    re_path(r'login/$', AccountLogin.as_view()),
]

urlpatterns += accounts.urls
