# from django.shortcuts import render, get_object_or_404
from django.contrib.auth import authenticate

from rest_framework import serializers
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework import generics, mixins, viewsets

from rest_framework_jwt.settings import api_settings

from . serializers import AccountSerializer

from django.contrib.auth.models import User


class AccountRegistration(generics.CreateAPIView):
    """
    @brief      Class for registration.
    """
    serializer_class = AccountSerializer
    permission_classes = (AllowAny, )


class AccountLogin(generics.CreateAPIView):
    """
    @brief      Class for logging-in.
    """
    serializer_class = AccountSerializer
    permission_classes = (AllowAny, )

    def create(self, request):
        """
        :param request: {'email': 'example.com', 'password': 'pass1234'}
        :return:  {'token': 'abcdef123456'}
        """
        print('===Request Data===')
        print(request.data)
        account = authenticate(**request.data)
        if not account:
            raise serializers.ValidationError({'error': 'Incorrect Username or Password'})
        pre_payload = api_settings.JWT_PAYLOAD_HANDLER(account)
        token = api_settings.JWT_ENCODE_HANDLER(pre_payload)
        token = api_settings.JWT_RESPONSE_PAYLOAD_HANDLER(token)
        return Response(token)


class AccountViewSet(mixins.ListModelMixin,
                     mixins.RetrieveModelMixin,
                     mixins.UpdateModelMixin,
                     mixins.DestroyModelMixin,
                     viewsets.GenericViewSet):
    """
    @brief      Class for registration.
    """
    queryset = User.objects.all()
    serializer_class = AccountSerializer
    permission_classes = (AllowAny, )
