import jwt
from calendar import timegm
from datetime import datetime, timedelta
from django.contrib.auth import  get_user_model
from django.utils.translation import ugettext as _
from rest_framework import serializers
from .compat import Serializer
from rest_framework_jwt.settings import api_settings
from rest_framework_jwt.compat import get_username_field
from .backends import HashModelBackend

User = get_user_model()
jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER
jwt_decode_handler = api_settings.JWT_DECODE_HANDLER
jwt_get_username_from_payload = api_settings.JWT_PAYLOAD_GET_USERNAME_HANDLER

#사용자(디테일)
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model=User
        fields = ['username','name','picture']

class WriterSerializer(serializers.ModelSerializer):
    class Meta:
        model=User
        fields = ['name']
#Access Token
class JSONWebTokenSerializer(Serializer):
    def __init__(self, *args, **kwargs):

        super(JSONWebTokenSerializer, self).__init__(*args, **kwargs)

        self.fields[self.username_field] = serializers.CharField()

    @property
    def username_field(self):
        return get_username_field()

    def validate(self, attrs):
        credentials = {
            self.username_field: attrs.get(self.username_field)
        }
        if all(credentials.values()):
            user = HashModelBackend.authenticate(self,username=attrs.get(self.username_field))
            if user:
                if not user.is_active:
                    msg = _('User account is disabled.')
                    raise serializers.ValidationError(msg)

                payload = jwt_payload_handler(user)
                access_token= jwt_encode_handler(payload)
                access_exp=api_settings.JWT_EXPIRATION_DELTA
                access_exp = (access_exp.days * 24 * 3600 +
                                access_exp.seconds)
                new_payload=payload
                refresh_limit=api_settings.JWT_REFRESH_EXPIRATION_DELTA
                refresh_limit = (refresh_limit.days * 24 * 3600 +
                                 refresh_limit.seconds)
                orig_iat=payload.get('orig_iat')
                new_payload['exp']=orig_iat+refresh_limit
                refresh_token=jwt_encode_handler(new_payload)
                return {
                    'access_token': access_token,
                    'refresh_token': refresh_token,
                    'user': user,
                    'exp':access_exp
                }
            else:
                msg = _('Unable to log in with provided credentials.')
                raise serializers.ValidationError(msg)
        else:
            msg = _('Must include "{username_field}" and "password".')
            msg = msg.format(username_field=self.username_field)
            raise serializers.ValidationError(msg)


#Refresh Token으로 만료시간 확인하고 Access Token 반환
class VerificationBaseSerializer(Serializer):
    """
    Abstract serializer used for verifying and refreshing JWTs.
    """
    token = serializers.CharField()

    def validate(self, attrs):
        msg = 'Please define a validate method.'
        raise NotImplementedError(msg)

    def _check_payload(self, token):
        try:
            payload = jwt_decode_handler(token)
        except jwt.ExpiredSignature:
            msg = _('Signature has expired.')
            raise serializers.ValidationError(msg)
        except jwt.DecodeError:
            msg = _('Error decoding signature.')
            raise serializers.ValidationError(msg)

        return payload

    def _check_user(self, payload):
        username = jwt_get_username_from_payload(payload)

        if not username:
            msg = _('Invalid payload.')
            raise serializers.ValidationError(msg)

        # Make sure user exists
        try:
            user = User.objects.get_by_natural_key(username)
        except User.DoesNotExist:
            msg = _("User doesn't exist.")
            raise serializers.ValidationError(msg)

        if not user.is_active:
            msg = _('User account is disabled.')
            raise serializers.ValidationError(msg)

        return user


class VerifyJSONWebTokenSerializer(VerificationBaseSerializer):
    """
    Check the veracity of an access token.
    """

    def validate(self, attrs):
        token = attrs['token']

        payload = self._check_payload(token=token)
        user = self._check_user(payload=payload)
        orig_iat = payload.get('orig_iat')
        if orig_iat:
            # Verify expiration
            access_limit = api_settings.JWT_EXPIRATION_DELTA

            if isinstance(access_limit, timedelta):
                access_limit = (access_limit.days * 24 * 3600 +
                                 access_limit.seconds)

            expiration_timestamp = orig_iat + int(access_limit)
            now_timestamp = timegm(datetime.utcnow().utctimetuple())

            if now_timestamp > expiration_timestamp:
                msg = _('Refresh has expired.')
                raise serializers.ValidationError(msg)
        else:
            msg = _('orig_iat field is required.')
            raise serializers.ValidationError(msg)

        new_payload = jwt_payload_handler(user)
        new_payload['orig_iat'] = orig_iat
        new_payload['exp'] = orig_iat + access_limit
        return {
            'token': jwt_encode_handler(new_payload),
            'user': user,
            'exp': access_limit
        }


class RefreshJSONWebTokenSerializer(VerificationBaseSerializer):
    """
    Refresh an access token.
    """

    def validate(self, attrs):
        token = attrs['token']

        payload = self._check_payload(token=token)
        user = self._check_user(payload=payload)
        orig_iat = payload.get('orig_iat')

        if orig_iat:
            refresh_limit = api_settings.JWT_REFRESH_EXPIRATION_DELTA
            if isinstance(refresh_limit, timedelta):
                refresh_limit = (refresh_limit.days * 24 * 3600 +
                                 refresh_limit.seconds)

            expiration_timestamp = orig_iat + int(refresh_limit)
            now_timestamp = timegm(datetime.utcnow().utctimetuple())
            if now_timestamp > expiration_timestamp:
                msg = _('Refresh has expired.')
                raise serializers.ValidationError(msg)
        else:
            msg = _('orig_iat field is required.')
            raise serializers.ValidationError(msg)

        new_payload = jwt_payload_handler(user)
        new_payload['orig_iat'] = orig_iat
        new_payload['exp'] = orig_iat+refresh_limit
        return {
            'token': jwt_encode_handler(new_payload),
            'user': user
        }
