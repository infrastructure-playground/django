# from django.shortcuts import render, get_object_or_404
from django.contrib.auth import authenticate

from rest_framework import serializers
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework import generics, mixins, viewsets

from rest_framework_jwt.settings import api_settings

from .serializers import AccountSerializer

from django.contrib.auth.models import User

# from utils.functions import check_google_recaptcha
from utils import constants


class AccountRegistration(generics.CreateAPIView):
    """
    @brief      Class for registration.
    """

    serializer_class = AccountSerializer
    permission_classes = (AllowAny,)


class AccountLogin(generics.CreateAPIView):
    """
    @brief      Class for logging-in.
    """

    serializer_class = AccountSerializer
    permission_classes = (AllowAny,)

    def create(self, request, *args, **kwargs):
        """
        :param request: {'username': 'armadadean',
                         'password': 'pass1234',
                         'token': 'xxxx'}
        :return:  {'token': 'abcdef123456'}
        """
        # token = request.data['token']
        # if not check_google_recaptcha(token, 'LOGIN'):
        #     # TODO SAME ACTION CONDITIONAL
        #     raise serializers.ValidationError({'error': constants.ERROR_CAPTCHA})
        # username = request.data['username']
        # password = request.data['password']
        # account = authenticate(username=username, password=password)
        account = authenticate(**request.data)
        if not account:
            raise serializers.ValidationError({'error': constants.ERROR_AUTH})
        pre_payload = api_settings.JWT_PAYLOAD_HANDLER(account)
        token = api_settings.JWT_ENCODE_HANDLER(pre_payload)
        token = api_settings.JWT_RESPONSE_PAYLOAD_HANDLER(token)
        return Response(token)


class AccountViewSet(
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet,
):
    """
    @brief      Class for registration.
    """

    queryset = User.objects.all()
    serializer_class = AccountSerializer
    permission_classes = (AllowAny,)
