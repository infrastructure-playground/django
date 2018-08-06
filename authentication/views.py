# from django.shortcuts import render, get_object_or_404

from rest_framework.permissions import AllowAny
from rest_framework import generics, mixins, viewsets

from .serializers import AccountSerializer
from authentication.models import Account


class AccountRegistration(generics.CreateAPIView):
    """
    @brief      Class for registration.
    """

    serializer_class = AccountSerializer
    permission_classes = (AllowAny, )


class AccountViewSet(mixins.ListModelMixin,
                     mixins.RetrieveModelMixin,
                     mixins.UpdateModelMixin,
                     mixins.DestroyModelMixin,
                     viewsets.GenericViewSet):
    """
    @brief      Class for registration.
    """

    queryset = Account.objects.all()
    serializer_class = AccountSerializer
    permission_classes = (AllowAny, )
