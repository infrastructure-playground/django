from rest_framework import serializers
from rest_framework_jwt.settings import api_settings

from . models import Account
# from core.functions import serializer_empty_cleaner


class AccountSerializer(serializers.ModelSerializer):
    """
    @brief      Class for account serializer.
    """
    password = serializers.CharField()
    confirm_password = serializers.CharField(required=False)
    # TODO: configure user update especially with the password

    class Meta:
        model = Account
        exclude = ('is_admin', 'created_at', 'updated_at')
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
        try:
            account = Account.objects.create_user(**validated_data)
            pre_payload = api_settings.JWT_PAYLOAD_HANDLER(account)
            token = api_settings.JWT_ENCODE_HANDLER(pre_payload)
            account.token = api_settings.JWT_RESPONSE_PAYLOAD_HANDLER(token)
        except ValueError as e:
            raise serializers.ValidationError({'error': e})
        # TODO do oauth token creation
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
        print('===TO REPRESENTATION INSTANCE===')
        print(instance.__dict__)
        if getattr(instance, 'token', None):
            ret = instance.token
        else:
            ret = super(AccountSerializer, self).to_representation(instance)
            ret.pop('password', None)
        # ret = serializer_empty_cleaner(ret)
        return ret
