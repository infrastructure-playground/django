from rest_framework import serializers
from rest_framework_jwt.settings import api_settings

# from . models import Account
from django.contrib.auth.models import User
# from core.functions import serializer_empty_cleaner


class AccountSerializer(serializers.ModelSerializer):
    """
    @brief      Class for account serializer.
    """
    password = serializers.CharField()
    confirm_password = serializers.CharField(required=False)
    # TODO: configure user update especially with the password

    class Meta:
        model = User
        fields = '__all__'
        # extra kwargs is declared to include both fields without putting it
        # to Meta fields attribute
        extra_kwargs = {
            'password': {'write_only': True},
            'confirm_password': {'write_only': True},
        }

    def create(self, validated_data):
        """
        @brief      account registration logic.
        """
        if validated_data['password'] != validated_data['confirm_password']:
            raise serializers.ValidationError({'error': 'Passwords must match'})
        else:
            del validated_data['confirm_password']
        account = User.objects.create_user(**validated_data)
        pre_payload = api_settings.JWT_PAYLOAD_HANDLER(account)
        token = api_settings.JWT_ENCODE_HANDLER(pre_payload)
        account.token = api_settings.JWT_RESPONSE_PAYLOAD_HANDLER(token)
        return account

    def delete(self, validated_data):
        """
        @TODO
        @brief
            - temporarily delete set it to inactive
            - permanent delete for delete request again on inactive user
        """
        return

    def to_representation(self, instance):
        if getattr(instance, 'token', None):
            ret = instance.token
        else:
            ret = super(AccountSerializer, self).to_representation(instance)
            ret.pop('password', None)
        return ret
