from django.urls import re_path

from rest_framework.routers import DefaultRouter

from . views import AccountRegistration, AccountViewSet


accounts = DefaultRouter()
accounts.register(r'', AccountViewSet)

app_name = 'authentication'
urlpatterns = [
    re_path(r'register/$', AccountRegistration.as_view()),
]

urlpatterns += accounts.urls
